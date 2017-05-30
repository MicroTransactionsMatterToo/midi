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
from typing import List, Dict


class LengthException(Exception):
    pass


class IntBuilder:
    original_data = None  # type: bytearray
    c_type = None  # type: str
    byte_length = None  # type: int
    little_endian = None  # type: int
    big_endian = None  # type: int

    def __init__(self, input_bytes: bytearray) -> None:
        # Set byte_length
        self.byte_length = len(input_bytes) * 8
        # Set the c_type field based on size of bytearray
        self.original_data = input_bytes
        if 32 <= self.byte_length * 8 < 64:
            self.c_type = "uint64"
        elif 16 <= self.byte_length * 8 < 32:
            self.c_type = "uint32"
        elif 8 <= self.byte_length * 8 < 16:
            self.c_type = "uint16"
        elif 4 <= self.byte_length * 8 < 8:
            self.c_type = "uint8"
        elif 2 <= self.byte_length * 8 < 4:
            self.c_type = "short"
        elif 1 <= self.byte_length * 8 < 2:
            self.c_type = "char"
        elif self.byte_length == 0:
            raise LengthException("Can't build Int with bytearray of size 0")
        else:
            self.c_type = None

        # Build the integer
        for index, byte in enumerate(input_bytes):
            # Calculate bit-shifting width
            shift_be = ((self.byte_length - 1) - index) * 8  # type: int
            shift_le = index * 8  # type: int
            self.little_endian <<= shift_le
            self.big_endian <<= shift_be
            self.little_endian |= byte
            self.big_endian |= byte

