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
from io import BufferedReader, FileIO
from typing import Union, Dict, List

from midisnake.structure import Track, Header, VariableLengthValue

__all__ = ["Parser"]


class Parser:
    midi_file = None  # type: Union[BufferedReader, FileIO]

    current_position = None  # type: int
    current_chunk = None  # type: int
    chunk_positions = []  # type: List[int]

    header = None  # type: Header
    tracks = []  # type: List[Track]

    def __init__(self, midi_file: BufferedReader) -> None:
        self.midi_file = midi_file
        self.header = Header(self.midi_file)

    def _read_track(self):
        self.chunk_positions.append(self.midi_file.tell())

        new_track = Track(self.midi_file)
