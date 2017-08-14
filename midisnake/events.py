#                       MIT License
# 
# Copyright (c) 15/08/17 Ennis Massey
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

from midisnake.structure import Event

note_values = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B"
}


def get_note_name(data: int) -> str:
    """
    Converts a MIDI note value to a note name.
    Args:
        data (int): Note value

    Returns:
        str: Note name
    """
    if data in range(0, 12):
        return note_values[data]
    else:
        return note_values[data % 12]


class NoteOn(Event):
    event_name = "NoteOn"
    indicator_byte = 0x90

    note_number = None  # type: int
    note_name = None  # type: str

    note_velocity = None  # type: int

    channel_number = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.note_number = data_array[1]
        self.note_name = get_note_name(data_array[1])
        self.note_velocity = data_array[2]


class NoteOff(Event):
    event_name = "NoteOff"
    indicator_byte = 0x80

    note_number = None  # type: int
    note_name = None  # type: str

    note_velocity = None  # type: int

    channel_number = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.note_number = data_array[1]
        self.note_name = get_note_name(data_array[1])
        self.note_velocity = data_array[2]