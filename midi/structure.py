#                       MIT License
# 
# Copyright (c) 13/01/17 Ennis Massey
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
from typing import AnyStr, List, Dict, Any, cast
from io import BufferedReader
from abc import ABCMeta, abstractmethod

__all__ = ["Header", "Event"]


class Header:
    __slots__ = ["length", "format", "ntrks", "division"]


class Event(metaclass=ABCMeta):  # pramga: no cover
    __slots__ = ["event_name"]

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "<MIDIEvent: {}>".format(self.event_name)

    def __str__(self) -> str:
        return "MIDIEvent: {}".format(self.event_name)

    @abstractmethod
    def process(self, data: int) -> None:
        pass


class Track:
    __slots__ = ["track_number", "length", "events"]


# class ValueSet:
#     integer: Dict[int, int]
#     string: Dict[str, str]
#     raw: Any
#
#     def __init__(self, data: Any) -> None:
#         if type(data) is str:
#             cast(str, data)
#             # Set the String values
#             self.string = {
#                 "ASCII": data.encode("ascii"),
#                 "UTF8": data.encode("utf-8"),
#                 "SHIFT-JIS": data.encode("shift-jis")
#             }
#             self.integer = {}
#             self.raw = data  # type: str


class VariableLengthValue:
    __slots__ = ['length', 'raw_data', 'value']

    def __init__(self, file_io: BufferedReader) -> None:
        # ---- Initialise values ---- #
        self.length = 0
        self.raw_data = bytearray()
        self.value = 0

        # ---- Parse value ---- #
        # Fetch one byte
        self.value = file_io.read(1)[0]  # type: int
        self.raw_data.append(self.value)
        self.length += 1
        # If not 0, the value is more than one byte
        if self.value & 0x80 > 0:
            # Split off indicator byte
            self.value &= 0x7F
            while True:
                current_byte = file_io.read(1)[0]  # type: int
                self.raw_data.append(current_byte)
                self.length += 1
                self.value <<= 7
                self.value |= (current_byte & 0x7F)
                if current_byte & 0x80 == 0:
                    break
