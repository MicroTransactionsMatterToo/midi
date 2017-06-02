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
from typing import List
from io import BufferedReader
from abc import ABCMeta, abstractmethod

__all__ = ["Header", "Event"]


class Header:
    length = None  # type: int
    format = None  # type: int
    ntrks  = None  # type: int
    division = None  # type: float


class Event(metaclass=ABCMeta):  # pramga: no cover
    event_name = None  # type: str

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
    track_number = None  # type: int
    length = None  # type: int
    events = None  # type: List[Event]



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
    """Parses and stores a MIDI variable length value
    
    Attributes:
        length (int): Length, in bytes, of value
        raw_data (bytearray): raw data read from file
        value (int): Final parsed value
    """
    length = None  # type: int
    raw_data = None   # type: bytearray
    value = None  # type: int


    def __init__(self, file_io: BufferedReader) -> None:
        """
        Parses a MIDI variable length value (VLV), and returns its length        
        Args:
            file_io (BufferedReader): Binary file object storing MIDI data 
        """
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
