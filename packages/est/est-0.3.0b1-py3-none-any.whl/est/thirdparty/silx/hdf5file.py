# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["W. de Nolf"]
__license__ = "MIT"
__date__ = "25/08/2020"


import h5py
import os
from contextlib import contextmanager, ExitStack
import traceback
import errno
import threading
import time
from silx.io import utils as silx_utils

HASSWMR = h5py.version.hdf5_version_tuple >= h5py.get_config().swmr_min_hdf5_version


class SharedLockPool:
    """
    Allows to acquire locks identified by name (hashable type) recursively.
    """

    def __init__(self):
        self.__locks = {}
        self.__locks_mutex = threading.Semaphore(value=1)

    def __len__(self):
        return len(self.__locks)

    @property
    def names(self):
        return list(self.__locks.keys())

    @contextmanager
    def _modify_locks(self):
        self.__locks_mutex.acquire()
        try:
            yield self.__locks
        finally:
            self.__locks_mutex.release()

    @contextmanager
    def acquire(self, name):
        with self._modify_locks() as locks:
            lock = locks.get(name, None)
            if lock is None:
                locks[name] = lock = threading.RLock()
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
            with self._modify_locks() as locks:
                locks.pop(name)

    @contextmanager
    def acquire_context_creation(self, name, contextmngr, *args, **kwargs):
        """
        Acquire lock only during context creation.

        This can be used for example to protect the opening of a file
        but not hold the lock while the file is open.
        """
        with ExitStack() as stack:
            with self.acquire(name):
                ret = stack.enter_context(contextmngr(*args, **kwargs))
            yield ret


class HDF5File(h5py.File):
    """File to secure reading and writing within h5py

    code originally from bliss.nexus_writer_service.io.nexus
    """

    _LOCKPOOL = SharedLockPool()

    def __init__(self, filename, mode, enable_file_locking=None, swmr=None, **kwargs):
        """
        :param str filename:
        :param str mode:
        :param bool enable_file_locking: by default it is disabled for `mode=='r'`
                                         and enabled in all other modes
        :param bool swmr: when not specified: try both modes when `mode=='r'`
        :param **kwargs: see `h5py.File.__init__`
        """
        if mode not in ("r", "w", "w-", "x", "a"):
            raise ValueError("invalid mode {}".format(mode))

        with self._protect_init(filename):
            # https://support.hdfgroup.org/HDF5/docNewFeatures/SWMR/Design-HDF5-FileLocking.pdf
            if not HASSWMR and swmr:
                swmr = False
            libver = kwargs.get("libver")
            if swmr:
                kwargs["libver"] = "latest"
            if enable_file_locking is None:
                enable_file_locking = mode != "r"
            old_file_locking = os.environ.get("HDF5_USE_FILE_LOCKING", None)
            if enable_file_locking:
                os.environ["HDF5_USE_FILE_LOCKING"] = "TRUE"
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
            kwargs["track_order"] = True
            try:
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
                if mode != "r" and swmr:
                    # Try setting writing in SWMR mode
                    try:
                        self.swmr_mode = True
                    except Exception:
                        pass
            except OSError as e:
                if (
                    swmr is not None
                    or mode != "r"
                    or not HASSWMR
                    or not isErrno(e, errno.EAGAIN)
                ):
                    raise
                # Try reading with opposite SWMR mode
                swmr = not swmr
                if swmr:
                    kwargs["libver"] = "latest"
                else:
                    kwargs["libver"] = libver
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
            if old_file_locking is None:
                del os.environ["HDF5_USE_FILE_LOCKING"]
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = old_file_locking

    @contextmanager
    def _protect_init(self, filename):
        """Makes sure no other file is opened/created
        or protected sections associated to the filename
        are executed.
        """
        lockname = os.path.abspath(filename)
        with self._LOCKPOOL.acquire(None):
            with self._LOCKPOOL.acquire(lockname):
                yield

    @contextmanager
    def protect(self):
        """Protected section associated to this file."""
        lockname = os.path.abspath(self.filename)
        with self._LOCKPOOL.acquire(lockname):
            yield


def isErrno(e, errno):
    """
    :param OSError e:
    :returns bool:
    """
    # Because e.__cause__ is None for chained exceptions
    return "errno = {}".format(errno) in "".join(traceback.format_exc())


class HDF5TimeoutError(TimeoutError):
    pass


def retry_get_data(timeout=None):
    """Decorate method that open+read an HDF5 file that is being written too.
    When HDF5 IO fails (because the writer is modifying the file) the method
    will be retried.

    Note: the method needs to be idempotent.
    """

    def decorator(method):
        def wrapper(url, *args, **kw):
            os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
            t0 = time.time()
            while True:
                try:
                    with h5py.File(url.file_path(), mode="r") as f:
                        return method(url)
                except HDF5TimeoutError:
                    raise
                except Exception:
                    # TODO: check whether it comes from h5py
                    pass
                print(f"retry {method}")
                time.sleep(0.1)
                if timeout is not None and (time.time() - t0) > timeout:
                    raise HDF5TimeoutError

        return wrapper

    return decorator


@retry_get_data(timeout=0.5)
def get_data(url):
    return silx_utils.get_data(url)
