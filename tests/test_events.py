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
import logging
from unittest import TestCase, TestSuite
from unittest.mock import MagicMock, call

from midisnake.events import NoteOff, NoteOn, PolyphonicAftertouch, PitchBend
from midisnake.errors import LengthError


logger = logging.getLogger(__name__)

logger.info("test_events tests started")


class TestNoteOn(TestCase):
    def test_validate(self):
        logger.info("Starting NoteOn .valid function tests")
        test_val = NoteOn.valid(0x900000)
        self.assertTrue(test_val, "Generic MIDI NoteOn message failed validation. Value was 0x{:X}".format(test_val))
        test_val = NoteOn.valid(0x800000)
        self.assertFalse(test_val,
                         "Generic MIDI NoteOn message shouldn't have validated, but did. Value was 0x{:x}".format(
                             test_val)
                         )
        logger.info("NoteOn .valid test passed")
    def test_constructor(self):
        logger.info("Starting NoteOn constructor tests")
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
        # --- Exception Testing --- #
        logger.info("Starting NoteOn constructor exception tests")
        # Test Length Exceptions
        with self.assertRaises(LengthError,
                               msg="NoteOn did not raise LengthError when given value 0x123001929391923919"
                               ) as exc:
            NoteOn(0x123001929391923919)
        logger.exception(exc)
        with self.assertRaises(LengthError,
                               msg="NoteOn did not raise LengthError when given value 0x1"
                               ) as exc:
            NoteOn(0x1)
        logger.exception(exc)
        # Test validation exceptions
        with self.assertRaises(ValueError,
                               msg="NoteOn given invalid data did not raise ValueError. Value was 0x290011"
                               ) as exc:
            NoteOn(0x290011)
        logger.exception(exc)
        with self.assertRaises(ValueError,
                               msg="NoteOn given invalid data but did not raise ValueError. Value was 0x999999"
                               ) as exc:
            NoteOn(0x899999)
        logger.exception(exc)

        # --- Parsing Testing --- #
        logger.info("Starting NoteOn constructor parsing test")
        for channel in range(0, 9):
            channel_num = 0x900000 + (channel << 16)
            logger.debug("Testing constructor with value {:x}".format(channel_num))
            obj = NoteOn(channel_num)
            match_val = {
                'channel_number': channel,
                'note_name': 'C',
                'note_number': 0,
                'note_velocity': 0,
                'raw_data': channel_num
            }
            self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOn with channel value: {}, "
                                             "parsing failed".format(channel >> 16))

