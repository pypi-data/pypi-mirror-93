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
"""wrapper to the larch mback process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from est.core.process.process import _NexusSpectrumDef
from est.core.process.process import _NexusDatasetDef
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from larch.xafs.xafsft import xftf
from est.core.utils.symbol import ANGSTROM_CHAR
import multiprocessing
import functools
import logging
import numpy

_logger = logging.getLogger(__name__)

_DEBUG = True
if _DEBUG:
    from larch.symboltable import Group


def process_spectr_xftf(
    spectrum,
    configuration,
    overwrite=True,
    callbacks=None,
    output=None,
    output_dict=None,
):
    """

    :param spectrum: spectrum to process
    :type: :class:`.Spectrum`
    :param configuration: configuration of the pymca normalization
    :type: dict
    :param overwrite: False if we want to return a new Spectrum instance
    :type: bool
    :param callback: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug("start xftf on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if (
        not hasattr(spectrum, "k")
        or not hasattr(spectrum, "chi")
        or spectrum.k is None
        or spectrum.chi is None
    ):
        _logger.error(
            "k and/or chi is/are not specified, unable to compute "
            "xftf. Maybe you need to run autobk process before ?"
        )
        return None, None
    _conf = configuration
    if "xftf" in _conf:
        _conf = _conf["xftf"]
    opts = {}
    for opt_name in (
        "kmin",
        "kmax",
        "kweight",
        "dk",
        "dk2",
        "with_phase",
        "window",
        "rmax_out",
        "nfft",
        "kstep",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]
            if opt_name == "kweight":
                opts["kw"] = _conf[opt_name]
    if _DEBUG is True:
        assert isinstance(spectrum, Group)
    if overwrite:
        _spectrum = spectrum
    else:
        _spectrum = Spectrum().load_frm_dict(spectrum.to_dict())
    xftf(_spectrum, **opts)
    # handle chi(x) * k**k_weight plot with r max
    if hasattr(_spectrum, "k") and hasattr(_spectrum, "chi"):
        if "kweight" in opts:
            kweight = opts["kweight"]
        else:
            kweight = 0
        if (
            "_plot_chi_k_weighted_r_max" in _conf
            and _conf["_plot_chi_k_weighted_r_max"] is not None
        ):
            mask = _spectrum.k < _conf["_plot_chi_k_weighted_r_max"]
        else:
            mask = numpy.ones_like(_spectrum.k).astype(numpy.bool)
    _spectrum.masked_chi_weighted_k = _spectrum.chi[mask] * (
        _spectrum.k[mask] ** kweight
    )
    _spectrum.masked_k = _spectrum.k[mask]
    # handle ft plot with r max
    if hasattr(_spectrum, "r") and hasattr(_spectrum, "chir_mag"):
        if "_plot_chi_mag_r_max" in _conf and _conf["_plot_chi_mag_r_max"] is not None:
            mask = _spectrum.r < _conf["_plot_chi_mag_r_max"]
        else:
            mask = numpy.ones_like(_spectrum.r).astype(numpy.bool)
        _spectrum.masked_chir_mag = _spectrum.chir_mag[mask]
        _spectrum.masked_r = _spectrum.r[mask]

    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, _spectrum


def larch_xftf(xas_obj):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    mback_obj = Larch_xftf()
    return mback_obj.process(xas_obj=xas_obj)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


class Larch_xftf(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="xftf")
        self._plot_settings = {}

    def set_properties(self, properties):
        if "_larchSettings" in properties:
            self._settings = properties["_larchSettings"]
        if "plot_settings" in properties:
            self._plot_settings = properties["plot_settings"]

    def process(self, xas_obj):
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self._settings:
            _xas_obj.configuration["xftf"] = self._settings
        elif "xftf" not in _xas_obj.configuration:
            _xas_obj.configuration["xftf"] = {}

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.register_process(
            _xas_obj,
            data_keys=(
                _NexusDatasetDef(
                    "chir_im",
                    units="{}^(-3)".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}^{-3}",
                ),
                _NexusDatasetDef("chir_re"),
                _NexusDatasetDef(
                    "chir_mag",
                    units="{}^(-3)".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}^{-3}",
                ),
                _NexusDatasetDef(
                    "masked_chir_mag",
                    units="{}".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}",
                ),
                _NexusDatasetDef(
                    "r", units="{}".format(ANGSTROM_CHAR), units_latex="\mathring{A}"
                ),
                _NexusDatasetDef(
                    "masked_r",
                    units="{}".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}",
                ),
                _NexusDatasetDef(
                    "k",
                    units="{}^(-1)".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}^{-1}",
                ),
                _NexusDatasetDef(
                    "masked_k",
                    units="{}^(-1)".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}^{-1}",
                ),
                _NexusDatasetDef(
                    "masked_chi_weighted_k",
                    units="{}^(-2)".format(ANGSTROM_CHAR),
                    units_latex="\mathring{A}^{-2}",
                ),
            ),
            plots=(
                _NexusSpectrumDef(
                    signal="masked_chi_weighted_k",
                    axes=("masked_k",),
                    auxiliary_signals=None,
                    silx_style={"signal_scale_type": "linear"},
                    title="chi(k)*k^k_weight",
                    title_latex="\chi(k).k^{k\_weight}",
                ),
                _NexusSpectrumDef(
                    signal="masked_chir_mag",
                    axes=("masked_r",),
                    auxiliary_signals=None,
                    silx_style={"signal_scale_type": "linear"},
                    title="chir_mag",
                ),
            ),
        )
        return _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            for spectrum in xas_obj.spectra:
                process_spectr_xftf(
                    spectrum=spectrum,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=True,
                )
        else:
            from multiprocessing import Manager

            manager = Manager()
            output_dict = {}
            res_list = manager.list()
            for i_spect, spect in enumerate(xas_obj.spectra):
                res_list.append(None)
                output_dict[spect] = i_spect

            with multiprocessing.Pool(5) as p:
                partial_ = functools.partial(
                    process_spectr_xftf,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=False,
                    output=res_list,
                    output_dict=output_dict,
                )
                p.map(partial_, xas_obj.spectra)

            # then update local spectrum
            for spectrum, res in zip(xas_obj.spectra, res_list):
                spectrum.update(res)

    def definition(self):
        return "xftf calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    def program_name(self):
        return "larch_xftf"

    __call__ = process
