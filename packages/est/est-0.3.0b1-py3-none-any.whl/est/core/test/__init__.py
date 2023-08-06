# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2018 European Synchrotron Radiation Facility
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
__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/12/2019"


import logging
import unittest


_logger = logging.getLogger(__name__)


def suite():
    test_suite = unittest.TestSuite()

    from est.core.types import test as test_types

    test_suite.addTest(test_types.suite())

    from est.core.process import test as test_process

    test_suite.addTest(test_process.suite())

    from .test_types import suite as test_types_suite

    test_suite.addTest(test_types_suite())

    from .test_io import suite as test_io_suite

    test_suite.addTest(test_io_suite())

    return test_suite
