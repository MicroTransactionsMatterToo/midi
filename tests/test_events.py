#                       MIT License
# 
# Copyright (c) 24/08/17 Ennis Massey
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
from unittest.mock import MagicMock, call

from midisnake.events import NoteOff, NoteOn, PolyphonicAftertouch, PitchBend
from midisnake.errors import LengthError


class TestNoteOn(TestCase):
    def test_validate(self):
        test_val = NoteOn.valid(0x900000)
        self.assertTrue(test_val, "Generic MIDI NoteOn message failed validation. Value was 0x{:X}".format(test_val))
        test_val = NoteOn.valid(0x800000)
        self.assertFalse(test_val,
                         "Generic MIDI NoteOn message shouldn't have validated, but did. Value was 0x{:x}".format(
                             test_val)
                         )

    def test_constructor(self):
        # Test constructor of generic version
        test_val = NoteOn(0x900000)
        match_val = {
            'channel_number': 0,
            'note_name': 'C',
            'note_number': 0,
            'note_velocity': 0,
            'raw_data': 9437184
        }
        self.assertEqual(vars(test_val),
                         match_val, "MIDI NoteOn constructed from value 0x{:X} is incorrect".format(0x900000)
                         )
        # Test Length Exceptions
        with self.assertRaises(LengthError,
                               msg="NoteOn did not raise LengthError when given value 0x123001929391923919"
                               ) as exc:
            NoteOn(0x123001929391923919)

        with self.assertRaises(LengthError,
                               msg="NoteOn did not raise LengthError when given value 0x1"
                               ) as exc:
            NoteOn(0x1)


