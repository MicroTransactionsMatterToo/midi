#                       MIT License
#
# Copyright (c) 29/05/17 Ennis Massey
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
class LengthException(Exception):
    pass


class IntBuilder:
    original_data = None  # type: bytearray
    c_type = None  # type: str
    byte_length = None  # type: int
    little_endian = 0  # type: int
    big_endian = 0  # type: int

    def __init__(self, input_bytes: bytearray) -> None:
        # Set byte_length
        self.byte_length = len(input_bytes)
        # Set the c_type field based on size of bytearray
        self.original_data = input_bytes
        if 32 < self.byte_length * 8 <= 64:
            self.c_type = "uint64"
        elif 16 < self.byte_length * 8 <= 32:
            self.c_type = "uint32"
        elif 8 < self.byte_length * 8 <= 16:
            self.c_type = "uint16"
        elif 4 < self.byte_length * 8 <= 8:
            self.c_type = "uint8"
        elif self.byte_length == 0:
            raise LengthException("Can't build Int with bytearray of size 0")
        else:
            self.c_type = None

        # Write ints
        self.big_endian = int.from_bytes(input_bytes, "big")
        self.little_endian = int.from_bytes(input_bytes, "little")

    def __repr__(self) -> str:
        return "<midi.integers.IntBuilder at 0x{id_hex:x}, raw: 0x{raw_val}, little endian: {little_endian}, " \
               "big endian: " \
               "{big_endian}, byte length: {byte_length}, C type: {c_type}>".format(
            id_hex=id(self), raw_val=str(''.join([hex(x)[2:] for x in self.original_data])),
            little_endian=self.little_endian,
            big_endian=self.big_endian,
            byte_length=self.byte_length,
            c_type=self.c_type
        )

    def __str__(self) -> str:
        return "{le}LE : {be}BE : 0x{raw}B".format(le=self.little_endian, be=self.big_endian,
                                                   raw=str(''.join([hex(x)[2:] for x in self.original_data])))
