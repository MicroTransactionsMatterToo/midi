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

from midisnake.errors import LengthError

__all__ = ["Header", "Event"]


class ParsedMIDI:
    def __init__(self):
        pass


class Header:
    """
    Represents a MIDI file header
    
    Attributes:
        length (int): length in bytes of the file, minus the length of the header
        format (int): Type of MIDI file, can be one of 0, 1 or 2. 0 and 1 are single file MIDI songs, 2 is comprised 
            of multiple files
        ntrks (int): Number of :class:`Track` 's in the file
        division (float): 
    """
    length = None  # type: int
    format = None  # type: int
    ntrks = None  # type: int
    division = None  # type: float


class Event(metaclass=ABCMeta):
    """
    Metaclass representing a MIDI Event. Subclasses must implement the :func:`~_process` function

    Attributes:
        event_name (str): Name of event
        indicator_byte (int): Byte that indicates the MIDI Event type
        raw_data (int): Initial data from MIDI file
    """
    event_name = None  # type: str
    indicator_byte = None  # type: int
    raw_data = None  # type: int

    def __init__(self, data: int) -> None:
        self.raw_data = data
        if len(hex(data)[2:]) != 6:
            err_msg = "Length of given data is incorrect. The length is {} and it should be 6".format(
                len(hex(data)[2:]))
            raise LengthError(err_msg)
        if self.valid(data):
            self._process(data)
        else:
            err_msg = "{} given invalid data".format(type(self).__name__)
            raise ValueError(err_msg)


    def __repr__(self) -> str:
        return "<MIDIEvent: {}>".format(self.event_name)

    def __str__(self) -> str:
        return "MIDIEvent: {}".format(self.event_name)

    @classmethod
    def valid(cls, data: int) -> bool:
        """
        Used by the parser to determine if the event is applicable
        Args:
            data (int): bytes of event

        Returns:
            bool: Whether the event matches or not
        """
        return (cls.indicator_byte == (bytearray.fromhex(hex(data)[2:])[0] & 0xF0))

    @abstractmethod
    def _process(self, data: int) -> None:
        """
        Processes the given data. Data is in the form of the remaining bytes in the file

        Called internally by __init__
        
        Args:
            data (int): Data given to be processed. 
        """
        pass


class Track:
    """
    Represents a MIDI track
    
    Attributes:
        track_number (int): Track index. Must be 0 or more
        length (int): Length of the track in bytes
        events (List[Event]): List of events present in the track
    """
    track_number = None  # type: int
    length = None  # type: int
    events = None  # type: List[Event]


class VariableLengthValue:
    """Parses and stores a MIDI variable length value
    
    Attributes:
        length (int): Length, in bytes, of value
        raw_data (bytearray): raw data read from file
        value (int): Final parsed value
    """
    length = None  # type: int
    raw_data = None  # type: bytearray
    value = None  # type: int

    def __init__(self, file_io: BufferedReader) -> None:
        """
        Parses a MIDI variable length value (VLV), and returns its length        
        Args:
            file_io (BufferedReader): Binary file object storing MIDI data 
        """
        # ---- Initialise values ---- #
        self.length = 0  # type: int
        self.raw_data = bytearray()  # type: bytearray
        self.value = 0  # type: int

        # ---- Parse value ---- #
        # Fetch one byte
        self.value = file_io.read(1)[0]
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
