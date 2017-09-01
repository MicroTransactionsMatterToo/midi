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
        self.assertTrue(test_val, "Generic MIDI NoteOn message failed validation. Value was 0x{:X}".format(0x900000))
        test_val = NoteOn.valid(0x800000)
        self.assertFalse(test_val,
                         "Generic MIDI NoteOn message shouldn't have validated, but did. Value was 0x{:x}".format(
                             0x800000)
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
            raise exc

        with self.assertRaises(LengthError,
                               msg="NoteOn did not raise LengthError when given value 0x1"
                               ) as exc:
            NoteOn(0x1)
            logger.exception(exc)
            raise exc
        # Test validation exceptions
        with self.assertRaises(ValueError,
                               msg="NoteOn given invalid data did not raise ValueError. Value was 0x290011"
                               ) as exc:
            NoteOn(0x290011)
            logger.exception(exc)
            raise exc
        with self.assertRaises(ValueError,
                               msg="NoteOn given invalid data but did not raise ValueError. Value was 0x999999"
                               ) as exc:
            NoteOn(0x899999)
            logger.exception(exc)
            raise exc

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
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOn with channel value: {}, "
                                                       "parsing failed".format(channel))
            except Exception as exc:
                logger.exception(exc)

        for note_number in range(0, 128):
            note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            event_data = 0x900000 + (note_number << 8)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': note_names[note_number % 12],
                'note_number': note_number,
                'note_velocity': 0,
                'raw_data': event_data
            }
            obj = NoteOn(event_data)
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOn with note value: {}, "
                                                       "parsing failed".format(note_number))
            except Exception as exc:
                logger.exception(exc)
                raise exc

        for velocity in range(0, 128):
            event_data = 0x900000 + (velocity)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': 'C',
                'note_number': 0,
                'note_velocity': velocity,
                'raw_data': event_data
            }
            obj = NoteOn(event_data)
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOn with velocity value: {}, "
                                                       "parsing failed".format(velocity))
            except Exception as exc:
                logger.exception(exc)
                raise exc

    def tearDown(self):
        logger.info("Finished testing NoteOn constructor tests")


class TestNoteOff(TestCase):
    def test_validate(self):
        logger.info("Starting NoteOff .valid function tests")
        test_val = NoteOff.valid(0x800000)
        self.assertTrue(test_val, "Generic MIDI NoteOff message failed validation. Value was 0x{:X}".format(0x800000))
        test_val = NoteOff.valid(0x900000)
        self.assertFalse(test_val,
                         "Generic MIDI NoteOff message shouldn't have validated, but did. Value was 0x{:x}".format(
                             0x900000)
                         )
        logger.info("NoteOn .valid test passed")

    def test_constructor(self):
        logger.info("Starting NoteOff constructor tests")
        # Test constructor of generic version
        test_val = NoteOff(0x800000)
        match_val = {
            'channel_number': 0,
            'note_name': 'C',
            'note_number': 0,
            'note_velocity': 0,
            'raw_data': 8388608
        }
        self.assertEqual(vars(test_val),
                         match_val, "MIDI NoteOff constructed from value 0x{:X} is incorrect".format(0x800000)
                         )
        # --- Exception Testing --- #
        logger.info("Starting NoteOn constructor exception tests")
        # Test Length Exceptions
        with self.assertRaises(LengthError,
                               msg="NoteOff did not raise LengthError when given value 0x123001929391923919"
                               ) as exc:
            NoteOff(0x123001929391923919)
            logger.exception(exc)
            raise exc
        with self.assertRaises(LengthError,
                               msg="NoteOff did not raise LengthError when given value 0x1"
                               ) as exc:
            NoteOff(0x1)
            logger.exception(exc)
            raise exc
        # Test validation exceptions
        with self.assertRaises(ValueError,
                               msg="NoteOff given invalid data did not raise ValueError. Value was 0x290011"
                               ) as exc:
            NoteOff(0x290011)
        logger.exception(exc)
        with self.assertRaises(ValueError,
                               msg="NoteOff given invalid data but did not raise ValueError. Value was 0x999999"
                               ) as exc:
            NoteOff(0x999999)
            logger.exception(exc)
            raise exc

        # --- Parsing Testing --- #
        logger.info("Starting NoteOff constructor parsing test")
        for channel in range(0, 9):
            channel_num = 0x800000 + (channel << 16)
            logger.debug("Testing constructor with value {:x}".format(channel_num))
            obj = NoteOff(channel_num)
            match_val = {
                'channel_number': channel,
                'note_name': 'C',
                'note_number': 0,
                'note_velocity': 0,
                'raw_data': channel_num
            }
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOff with channel value: {}, "
                                                       "parsing failed".format(channel))
            except Exception as exc:
                logger.exception(exc)
                raise exc

        for note_number in range(0, 128):
            note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            event_data = 0x800000 + (note_number << 8)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': note_names[note_number % 12],
                'note_number': note_number,
                'note_velocity': 0,
                'raw_data': event_data
            }
            obj = NoteOff(event_data)
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOff with note value: {}, "
                                                       "parsing failed".format(note_number))
            except Exception as exc:
                logger.exception(exc)
                raise exc

        for velocity in range(0, 128):
            event_data = 0x800000 + (velocity)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': 'C',
                'note_number': 0,
                'note_velocity': velocity,
                'raw_data': event_data
            }
            obj = NoteOff(event_data)
            try:
                self.assertEqual(vars(obj), match_val, "When testing constructor of NoteOff with velocity value: {}, "
                                                       "parsing failed".format(velocity))
            except Exception as exc:
                logger.exception(exc)
                raise exc

    def tearDown(self):
        logger.info("Finished testing NoteOn constructor tests")


class TestPolyphonicAftertouch(TestCase):
    def setUp(self):
        logger.info("Starting Polyphonic Aftertouch tests")

    def test_validate(self):
        logger.info("Starting Polyphonic Aftertouch .valid function tests")
        test_val = PolyphonicAftertouch.valid(0xA00000)
        self.assertTrue(test_val,
                        "Generic MIDI PolyphonicAftertouch message failed validation. Value was 0x{:X}".format(
                            0xA00000))
        test_val = PolyphonicAftertouch.valid(0xB00000)
        self.assertFalse(test_val,
                         "Generic MIDI Polyphonic Aftertouch message shouldn't "
                         "have validated, but did. Value was 0x{:x}".format(
                             0xB00000)
                         )
        logger.info("Polyphonic Aftertouch .valid test passed")

    def test_constructor(self):
        logger.info("Starting PolyphonicAftertouch constructor tests")
        # Test constructor of generic version
        test_val = PolyphonicAftertouch(0xA00000)
        match_val = {
            'channel_number': 0,
            'note_name': 'C',
            'note_number': 0,
            'pressure': 0,
            'raw_data': 10485760
        }
        self.assertEqual(vars(test_val),
                         match_val,
                         "MIDI PolyphonicAftertouch constructed from value 0x{:X} is incorrect".format(0xA00000)
                         )
        # --- Exception Testing --- #
        logger.info("Starting PolyphonicAftertouch constructor exception tests")
        # Test Length Exceptions
        with self.assertRaises(LengthError,
                               msg="PolyphonicAftertouch did not raise LengthError when given value 0x123001929391923919"
                               ) as exc:
            PolyphonicAftertouch(0x123001929391923919)
            logger.exception(exc)
            raise exc
        with self.assertRaises(LengthError,
                               msg="PolyphonicAftertouch did not raise LengthError when given value 0x1"
                               ) as exc:
            PolyphonicAftertouch(0x1)
            logger.exception(exc)
            raise exc
        # Test validation exceptions
        with self.assertRaises(ValueError,
                               msg="PolyphonicAftertouch given invalid data did not raise ValueError. Value was 0x290011"
                               ) as exc:
            PolyphonicAftertouch(0x290011)
            logger.exception(exc)
            raise exc
        with self.assertRaises(ValueError,
                               msg="PolyphonicAftertouch given invalid data but did not raise ValueError. Value was 0x999999"
                               ) as exc:
            PolyphonicAftertouch(0x999999)
            logger.exception(exc)
            raise exc

        # --- Parsing Testing --- #
        logger.info("Starting PolyphonicAftertouch constructor parsing test")
        for channel in range(0, 9):
            channel_num = 0xA00000 + (channel << 16)
            logger.debug("Testing constructor with value {:x}".format(channel_num))
            obj = PolyphonicAftertouch(channel_num)
            match_val = {
                'channel_number': channel,
                'note_name': 'C',
                'note_number': 0,
                'pressure': 0,
                'raw_data': channel_num
            }
            try:
                self.assertEqual(vars(obj), match_val,
                                 "When testing constructor of PolyphonicAftertouch with channel value: {}, "
                                 "parsing failed".format(channel))
            except Exception as exc:
                logger.exception(exc)
                raise exc

        for note_number in range(0, 128):
            note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            event_data = 0xA00000 + (note_number << 8)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': note_names[note_number % 12],
                'note_number': note_number,
                'pressure': 0,
                'raw_data': event_data
            }
            obj = PolyphonicAftertouch(event_data)
            try:
                self.assertEqual(vars(obj), match_val,
                                 "When testing constructor of PolyphonicAftertouch with note value: {}, "
                                 "parsing failed".format(note_number))
            except Exception as exc:
                logger.exception(exc)
                raise exc

        for pressure in range(0, 128):
            event_data = 0xA00000 + (pressure)
            logger.debug("Testing constructor with value {:x}".format(event_data))
            match_val = {
                'channel_number': 0,
                'note_name': 'C',
                'note_number': 0,
                'pressure': pressure,
                'raw_data': event_data
            }
            obj = PolyphonicAftertouch(event_data)
            try:
                self.assertEqual(vars(obj), match_val,
                                 "When testing constructor of PolyphonicAftertouch with pressure value: {}, "
                                 "parsing failed".format(pressure))
            except Exception as exc:
                logger.exception(exc)
                raise exc
