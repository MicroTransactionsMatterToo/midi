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


def _decode_leftright(data: int) -> str:
    if data > 64:
        return "right"
    elif data < 64:
        return "left"
    elif data == 64:
        return "center"
    else:
        raise ValueError("Balance value {} was outside of valid range of 0-127".format(data))


midi_controls = {
    0x00: {
        "name": "Bank Select",
        "byteorder": "big"
    },
    0x01: {
        "name": "Modulation Wheel",
        "byteorder": "big"
    },
    0x02: {
        "name": "Breath Control",
        "byteorder": "big"
    },
    0x03: {
        "name": "undefined",
        "byteorder": "big"
    },
    0x04: {
        "name": "Foot Controller",
        "byteorder": "big"
    },
    0x05: {
        "name": "Portamento Time",
        "byteorder": "big"
    },
    0x06: {
        "name": "Data Entry",
        "byteorder": "big"
    },
    0x07: {
        "name": "Channel Volume",
        "byteorder": "big"
    },
    0x08: {
        "name": "Balance",
        "byteorder": "big",
        "decoder": _decode_leftright
    },
    0x09: {
        "name": "undefined",
        "byteorder": "big"
    },
    0x0A: {
        "name": "Pan",
        "byteorder": "big",
        "decoder": _decode_leftright
    },
    0x0B: {
        "name": "Expression",
        "byteorder": "big"
    },
    0x0C: {
        "name": "Effect Controller 1",
        "byteorder": "big"
    },
    0x0D: {
        "name": "Effect Controller 2",
        "byteorder": "big"
    },
    0x0E: {
        "name": "General Purpose",
        "byteorder": "big"
    },
    0x0F: {
        "name": "General Purpose",
        "byteorder": "big"
    },
    0x10: {
        "name": "General Purpose",
        "byteorder": "big"
    },
    0x11: {
        "name": "General Purpose",
        "byteorder": "big"
    },
    0x12: {
        "name": "General Purpose",
        "byteorder": "big"
    },
    0x13: {
        "name": "General Purpose",
        "byteorder": "big"
    }
}


def get_note_name(data: int) -> str:
    """Converts a MIDI note value to a note name.

    Arguments:
        data (int): Note value

    Returns:
        str: Note name
    
    Raises:
        ValueError: This is raised when the given value is smaller than 0, or larger than 127 (maximum value allowed 
        in specification)
    """
    # Raise ValueError if value is too large or too small
    if data > 127:
        raise ValueError("Note values cannot be larger than 127 (0x7F). Given value was {0} ({0:x})".format(data))
    if data < 0:
        raise ValueError("Note values cannot be smaller than 0 (0x00). Given value was {0} ({0:x})".format(data))
    if data in range(0, 12):
        return note_values[data]
    else:
        return note_values[data % 12]


class NoteOn(Event):
    """MIDI NoteOn event

    Notes:
        Subclasses the :class:`midisnake.structure.Event` metaclass

    Attributes:
        event_name (str): Name of Event
        indicator_byte (int): Byte that indicates the MIDI Event type
        note_number (int): MIDI note number, between 0 and 127
        note_name (str): Musical note name, as returned by :func:`get_note_name`
        note_velocity (int): Volume, between 0 and 127
        channel_number (int): MIDI Channel number
        raw_data (int): Initial data from MIDI file
    """
    event_name = "NoteOn"
    indicator_byte = 0x90

    note_number = None  # type: int
    note_name = None  # type: str

    note_velocity = None  # type: int

    channel_number = None  # type: int

    raw_data = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.note_number = data_array[1]
        self.note_name = get_note_name(data_array[1])
        self.note_velocity = data_array[2]
        self.raw_data = data


class NoteOff(Event):
    """MIDI NoteOff event

    Notes:
        Subclasses the :class:`midisnake.structure.Event` metaclass

    Attributes:
        event_name (str): Name of Event
        indicator_byte (int): Byte that indicates the MIDI Event type
        note_number (int): MIDI note number, between 0 and 127
        note_name (str): Musical note name, as returned by :func:`get_note_name`
        note_velocity (int): Volume, between 0 and 127
        channel_number (int): MIDI Channel number
        raw_data (int): Initial data from MIDI file
    """
    event_name = "NoteOff"
    indicator_byte = 0x80

    note_number = None  # type: int
    note_name = None  # type: str

    note_velocity = None  # type: int

    channel_number = None  # type: int

    raw_data = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.note_number = data_array[1]
        self.note_name = get_note_name(data_array[1])
        self.note_velocity = data_array[2]
        self.raw_data = data


class PolyphonicAftertouch(Event):
    """MIDI PolyPhonic Aftertouch

    Notes:
        Subclasses the :class:`midisnake.structure.Event` metaclass

    Attributes:
        event_name (str): Name of Event
        indicator_byte (int): Byte that indicates the MIDI Event type
        pressure (int): Polyphonic Pressure, between 0 and 16383
        channel_number (int): MIDI Channel number
        raw_data (int): Initial data from MIDI file
    """
    event_name = "Polyphonic Aftertouch"
    indicator_byte = 0xA0

    pressure = None  # type: int
    note_number = None  # type: int
    note_name = None  # type: str

    channel_number = None  # type: int

    raw_data = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.note_number = data_array[1]
        self.note_name = get_note_name(data_array[1])
        self.pressure = data_array[2]
        self.raw_data = data


class PitchBend(Event):
    """MIDI Pitch Bend 
    
    Notes:
        Subclasses the :class:`midisnake.structure.Event` metaclass
    
    Attributes:
        event_name (str): Name of Event
        indicator_byte (int): Byte that indicates the MIDI Event type
        channel_number (int): MIDI Channel number
        bend_amount (int): Amount of bend to apply
        raw_data (int): Initial data from MIDI file
    """
    event_name = "Pitch Bend"
    indicator_byte = 0xE0

    bend_amount = None  # type: int

    channel_number = None  # type: int

    raw_data = None  # type: int

    def _process(self, data: int):
        data_array = bytearray.fromhex(hex(data)[2:])
        self.channel_number = data_array[0] & 0x0F
        self.bend_amount = (data_array[2] << 7) & data_array[1]
        self.raw_data = data
