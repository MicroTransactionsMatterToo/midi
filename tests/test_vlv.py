#                       MIT License
# 
# Copyright (c) 30/05/17 Ennis Massey
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
from unittest import TestCase
from unittest.mock import MagicMock, call
from typing import Union
from io import BufferedReader

from midisnake.structure import VariableLengthValue


class TestVLV(TestCase):
    def setUp(self):
        self.mock_file = MagicMock()  # type: Union[BufferedReader, MagicMock]
        self.mock_file.read = MagicMock(side_effect=[b'\x84', b'\x18', b'\x00', b'\x3C'])  # type: MagicMock

    def tearDown(self):
        self.mock_file.reset_mock()

    def test_multi_byte_vlv(self):
        vlv_instance = VariableLengthValue(self.mock_file)
        self.assertEqual(vlv_instance.value, 536, "VLV Value Incorrect")
        self.assertEqual(vlv_instance.raw_data, bytearray(b'\x84\x18'), "VLV Read data incorrect")
        self.assertEqual(vlv_instance.length, 2, "VLV Length incorrect")
        self.mock_file.read.assert_has_calls([call(1), call(1)], "VLV read calls incorrect")

    def test_zero_value(self):
        self.mock_file.read = MagicMock(side_effect=[b'\x00'])
        vlv_instance = VariableLengthValue(self.mock_file)
        self.assertEqual(vlv_instance.value, 0, "VLV Incorrect value when reading from NULL byte")
        self.assertEqual(vlv_instance.length, 1, "VLV Incorrect data read (NULL byte test)")
        self.assertEqual(vlv_instance.raw_data, bytearray(b'\x00'), "VLV Incorrect length when reading NULL byte")
        self.mock_file.read.assert_has_calls([call(1)], "VLV Incorrect calls made when reading from NULL byte")

    def test_single_byte_vlv(self):
        self.mock_file.read = MagicMock(side_effect=[b'\x3C'])
        vlv_instance = VariableLengthValue(self.mock_file)
        self.assertEqual(vlv_instance.value, 60, "VLV Value incorrect when reading from single byte")
        self.assertEqual(vlv_instance.raw_data, bytearray(b'\x3C'), "VLV Incorrect data read from single byte")
        self.assertEqual(vlv_instance.length, 1, "VLV Incorrect length when reading single byte")
        self.mock_file.read.assert_has_calls([call(1)], "VLV Incorrect calls when reading from single byte")
