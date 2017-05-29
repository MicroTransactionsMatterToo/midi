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
from abc import ABC, abstractmethod

__all__ = ["Header", "Event"]


class Header:
    length = None  # type: int
    format = None  # type: int
    ntrks = None  # type: int
    division = None  # type: float


class Event(ABC):
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
    events = None  # type: Dict[int, List[Event]]


class ValueSet:
    integer = None  # type: Dict[int, int]
    string = None  # type: Dict[str, str]
    raw = None  # type: Any

    def __init__(self, data: Any) -> None:
        if type(data) is str:
            cast(str, data)
            # Set the String values
            self.string = {
                "ASCII": data.encode("ascii"),
                "UTF8": data.encode("utf-8"),
                "SHIFT-JIS": data.encode("shift-jis")
            }
            self.integer = {}
            self.raw = data  # type: str


class VariableLengthValue:
    length = None  # type: int
    raw_data = None  # type: bytearray
    values = None  # type: ValueSet
