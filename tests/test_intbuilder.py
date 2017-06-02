#                       MIT License
# 
# Copyright (c) 1/06/17 Ennis Massey
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

from midisnake.integers import IntBuilder, LengthException


class TestIntBuilder(TestCase):
    def test_repr(self):
        self.intb_inst = IntBuilder(bytearray(b'\x01\xA4'))
        memory_address = id(self.intb_inst)
        self.assertEqual(repr(self.intb_inst), "<midisnake.integers.IntBuilder at 0x{mem_addr:x}, raw: 0x1a4, "
                                               "little endian: "
                                               "41985, big endian: 420, byte length: 2, C type: uint16>".format(
            mem_addr=memory_address))
        self.intb_inst = IntBuilder(bytearray(b'\x2A'))
        memory_address = id(self.intb_inst)
        self.assertEqual(repr(self.intb_inst), "<midisnake.integers.IntBuilder at 0x{mem_addr:x}, raw: 0x2a, "
                                               "little endian: "
                                               "42, big endian: 42, byte length: 1, C type: uint8>".format(
            mem_addr=memory_address))

    def test_str(self):
        self.intb_inst = IntBuilder(bytearray(b'\x01\xA4'))
        memory_address = id(self.intb_inst)
        self.assertEqual(str(self.intb_inst), "41985LE : 420BE : 0x1a4B".format(
            mem_addr=memory_address))
        self.intb_inst = IntBuilder(bytearray(b'\x2A'))
        memory_address = id(self.intb_inst)
        self.assertEqual(str(self.intb_inst), "42LE : 42BE : 0x2aB".format(
            mem_addr=memory_address))

    def test_nullbyte(self):
        with self.assertRaises(LengthException):
            self.intb_inst = IntBuilder(bytearray(b''))

    def test_init(self):
        self.intb_inst = IntBuilder(bytearray(b'\x01\xA4'))
        self.assertEqual({
            'big_endian': self.intb_inst.big_endian,
            'byte_length': self.intb_inst.byte_length,
            'c_type': self.intb_inst.c_type,
            'little_endian': self.intb_inst.little_endian,
            'original_data': self.intb_inst.original_data
        }, {
            'big_endian': 420,
            'byte_length': 2,
            'c_type': 'uint16',
            'little_endian': 41985,
            'original_data': bytearray(b'\x01\xA4')
        })
        self.intb_inst = IntBuilder(bytearray(b'\x2A'))
        self.assertEqual({
            'big_endian': self.intb_inst.big_endian,
            'byte_length': self.intb_inst.byte_length,
            'c_type': self.intb_inst.c_type,
            'little_endian': self.intb_inst.little_endian,
            'original_data': self.intb_inst.original_data
        }, {
            'big_endian': 42,
            'byte_length': 1,
            'c_type': 'uint8',
            'little_endian': 42,
            'original_data': bytearray(b'\x2A')
        })
        self.intb_inst = IntBuilder(bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff'))
        self.assertEqual({
            'big_endian': self.intb_inst.big_endian,
            'byte_length': self.intb_inst.byte_length,
            'c_type': self.intb_inst.c_type,
            'little_endian': self.intb_inst.little_endian,
            'original_data': self.intb_inst.original_data
        }, {
            'big_endian': 18446744073709551615,
            'byte_length': 8,
            'c_type': 'uint64',
            'little_endian': 18446744073709551615,
            'original_data': bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff')
        })
        self.intb_inst = IntBuilder(bytearray(b'\xff\xff\xff\xff'))
        self.assertEqual({
            'big_endian': self.intb_inst.big_endian,
            'byte_length': self.intb_inst.byte_length,
            'c_type': self.intb_inst.c_type,
            'little_endian': self.intb_inst.little_endian,
            'original_data': self.intb_inst.original_data
        }, {
            'big_endian': 4294967295,
            'byte_length': 4,
            'c_type': 'uint32',
            'little_endian': 4294967295,
            'original_data': bytearray(b'\xff\xff\xff\xff')
        })
        self.intb_inst = IntBuilder(bytearray((999999999999999999).to_bytes(128, 'big')))
        self.assertEqual({
            'big_endian': self.intb_inst.big_endian,
            'byte_length': self.intb_inst.byte_length,
            'c_type': self.intb_inst.c_type,
            'little_endian': self.intb_inst.little_endian,
            'original_data': self.intb_inst.original_data
        }, {
            'big_endian': 999999999999999999,
            'byte_length': 128,
            'c_type': None,
            'little_endian': 179767638237020898356623490710434418536775593352576159933757128944707257350954536914063245326939442175767480235509437650677415131917209873130951247687383631600519862940215216702259024034572879454308448988996237931693908948093169681562364347544258390966030456380791142075624025472352408185492254992022911320064,
            'original_data': bytearray(
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\xe0\xb6\xb3\xa7c\xff\xff')
        })
