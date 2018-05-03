#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import sys
import unittest
import subprocess
from tests.context import sbpipe


class TestCopasiSim(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = 'config_errors'
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._ir_folder)
        try:
            subprocess.Popen(['CopasiSE'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'CopasiSE not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim1(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul1.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_sim2(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul2.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_sim3(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul3.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_sim4(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul4.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_sim5(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul5.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
