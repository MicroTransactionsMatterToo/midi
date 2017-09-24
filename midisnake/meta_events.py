#                       MIT License
# 
# Copyright (c) 20/09/17 Ennis Massey
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

"""
Provides functions for parsing of MIDI meta events
"""

from io import BufferedReader, FileIO
from typing import Union, Tuple, NamedTuple, Callable, Any

from midisnake.structure import VariableLengthValue
from midisnake.errors import EventLengthError, EventNullLengthError, EventTextError

SMPTE_Format = NamedTuple("SMPTE_Format",
                          [
                              ('hours', int),
                              ('minutes', int),
                              ('seconds', int),
                              ('fps', int),
                              ('ff', int)
                          ]
                          )  # type: Union[Callable, NamedTuple]


class MetaTextEvent:
    variant_number = None  # type: int
    variant_name = None  # type: str

    length = None  # type: int

    text = None  # type: str

    event_info = None  # type: bytearray
    raw_content = None  # type: bytearray

    def __init__(self, event_info: bytes, variant: int, data: Tuple[int, str, bytearray]) -> None:
        self.event_info = bytearray(event_info)
        self.variant_number = variant

        self.length = data[0] + len(event_info)
        self.raw_content = self.event_info + bytes(data[2])

        self.text = data[1]


class MetaSequenceNumber:
    sequence_number = None  # type: int

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, int, bytearray]):
        self.length, self.sequence_number, self.raw_content = data


class MetaKeySignature:
    signature_index = None  # type: int
    signature_name = None  # type: str

    major_minor = None  # type: bool

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, Tuple[int, int], bytearray]):
        self.raw_content = data[2]
        self.length = data[0]

        signature_names = ["Cb", "Fb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#"]

        if data[1][0] not in range(-7, 8):
            raise ValueError("Invalid Key Signature value")
        self.signature_index = data[1][0]
        self.signature_name = signature_names[self.signature_index + 7]


class MetaTimeSignature:
    numerator = None  # type: int
    denominator = None  # type: int

    clocks_per_tick = None  # type: int
    tsnotes_per_qnote = None  # type: int

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, Tuple[int, int, int, int], bytearray]):
        self.raw_content = data[2]
        self.length = data[0]

        self.numerator = data[1][0]
        self.denominator = data[1][1]

        self.clocks_per_tick = data[1][2]
        self.tsnotes_per_qnote = data[1][3]

    @property
    def parsed_signature(self) -> str:
        actual_denominator = 2 ** self.denominator
        return "{}/{}".format(self.numerator, actual_denominator)


class MetaSMPTEOffset:
    hours = None  # type: int
    minutes = None  # type: int
    seconds = None  # type: int
    fps = None  # type: int
    fractional_frames = None  # type: int

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, Tuple[int, int, int, int, int], bytearray]):
        self.hours, self.minutes, self.seconds, self.fps, self.ff = data[1]

        self.length = data[0]
        self.raw_content = data[1]


class MetaSetTempo:
    tpqm = None  # type: int

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, int, bytearray]):
        self.length, self.tpqm, self.raw_content = data

    def get_tempo(self):
        return self.tpqm / 60000000.0


class MetaChannelPrefix:
    prefix = None  # type: int

    length = None  # type: int
    raw_content = None  # type: bytearray

    def __init__(self, data: Tuple[int, int, bytearray]):
        self.length, self.prefix, self.raw_content = data


class EndOfTrack:
    length = None  # type: int

    def __init__(self, data: Tuple[int, None, None]):
        self.length = data[0]


def sequence_number(data: Union[FileIO, BufferedReader]) -> Tuple[int, int, bytearray]:
    length_bytes = bytearray(data.read(4))
    length = int.from_bytes(length_bytes, "big")
    if length != 2:
        raise EventLengthError("Sequence Number length was incorrect. It should be 2, but it was {}".format(length))
    sequence_num_raw = bytearray(data.read(2))
    sequence_num = int.from_bytes(sequence_num_raw, "big")
    return length, sequence_num, sequence_num_raw


def text_event(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparsable text in text event") from exc

    return length, text, raw_data


def copyright_notice(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparsable text in copyright notice") from exc

    return length, text, raw_data


def chunk_name(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparsable text in track/sequence name") from exc

    return length, text, raw_data


def instrument_name(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparsable text in instrument name") from exc

    return length, text, raw_data


def lyric(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparseable text in lyric text") from exc

    return length, text, raw_data


def marker(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparseable text in marker text") from exc

    return length, text, raw_data


def cue_point(data: Union[FileIO, BufferedReader]) -> Tuple[int, str, bytearray]:
    length = VariableLengthValue(data).value
    raw_data = bytearray(data.read(length))
    try:
        text = raw_data.decode("ASCII")
    except UnicodeDecodeError as exc:
        raise EventTextError("Unparseable text in Cue Point text") from exc

    return length, text, raw_data


def channel_prefix(data: Union[FileIO, BufferedReader]) -> Tuple[int, int, bytearray]:
    length_bytes = data.read(4)
    length = int.from_bytes(length_bytes, "big")
    if length != 0x01:
        raise EventLengthError("Channel Prefix length invalid. It should be 1, but it's {}".format(length))
    prefix_raw = bytearray(data.read(1))
    prefix = int.from_bytes(prefix_raw, "big")

    return length, prefix, prefix_raw


def end_of_track(data: Union[FileIO, BufferedReader]) -> Tuple[int, None, None]:
    length_bytes = data.read(4)
    length = int.from_bytes(length_bytes, "big")
    if length != 0:
        raise EventLengthError("End of Track event with non-zero length")
    return length, None, None


def set_tempo(data: Union[FileIO, BufferedReader]) -> Tuple[int, int, bytearray]:
    length_bytes = data.read(4)
    length = int.from_bytes(length_bytes, "big")
    if length != 3:
        raise EventLengthError("Set Tempo event with length other than 3. Given length was {}".format(length))
    raw_data = bytearray(data.read(3))
    tpqm = int.from_bytes(raw_data, "big")

    return length, tpqm, raw_data


def smpte_offset(data: Union[FileIO, BufferedReader]) -> Tuple[int, Tuple[int, int, int, int, int], bytearray]:
    length_bytes = data.read(4)
    length = int.from_bytes(length_bytes, "big")
    if length != 0x05:
        raise EventLengthError("SMPTE Offset length is not 5. Given value was {}".format(length))

    # Process Hours
    hour_data = bytearray(data.read(8))
    hour_bits = int.from_bytes(hour_data, 'big')
    null_bit = hour_bits & 0b10000000

    frame_crumb = (hour_bits & 0b01100000) >> 5
    hours = hour_bits & 0b00011111

    minute_data = bytearray(data.read(8))
    minute_bits = int.from_bytes(minute_data, "big")
    null_bit |= minute_bits & 0b11000000
    minutes = minute_bits & 0b00111111

    second_data = bytearray(data.read(8))
    second_bits = int.from_bytes(second_data, "big")
    null_bit |= second_bits & 0b11000000
    seconds = second_bits & 0b00111111

    frame_count_data = bytearray(data.read(8))
    frame_count_bits = int.from_bytes(frame_count_data, "big")
    null_bit = frame_count_bits & 0b11100000
    frame_count = frame_count_bits & 0b00011111

    fraction_data = bytearray(data.read(8))
    fraction = int.from_bytes(fraction_data, "big")

    raw_data = bytearray()
    [raw_data.append(x) for x in [hour_bits, minute_bits, second_bits, frame_count_bits, fraction]]

    smpte_data = SMPTE_Format(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        fps=frame_count,
        ff=fraction
    )

    if null_bit != 0b0:
        raise ValueError("Null bits were not 0 in SMPTE timecode")

    return length, smpte_data, raw_data


def time_signature(data: Union[FileIO, BufferedReader]) -> Tuple[int, Tuple[int, int, int, int], bytearray]:
    length_bytes = bytearray(data.read(1))
    length = int.from_bytes(length_bytes, "big")

    if length != 0x04:
        raise EventLengthError("Time Signature event has invalid length. Should be 4, value was {}".format(length))

    data_bytes = bytearray(data.read(4))  # type: bytearray
    numerator = data_bytes[0]  # type: int
    denominator = data_bytes[1]  # type: int
    clock_num = data_bytes[2]
    ts_number = data_bytes[3]

    return length, (numerator, denominator, clock_num, ts_number), data_bytes


def key_signature(data: Union[FileIO, BufferedReader]) -> Tuple[int, Tuple[int, int], bytearray]:
    length_bytes = bytearray(data.read(1))
    length = int.from_bytes(length_bytes, "big")

    if length != 0x02:
        raise EventLengthError("Key Signature event has invalid length. Should be 2, value was {}".format(length))

    data_bytes = bytearray(data.read(2))
    signature_index = data_bytes[0]
    minor_major = data_bytes[1]

    return length, (signature_index, minor_major), data_bytes


meta_events = {
    0x00: {
        "function": sequence_number,
        "object_type": MetaSequenceNumber
    },
    0x01: {
        "function": text_event,
        "object_type": MetaTextEvent
    },
    0x02: {
        "function": copyright_notice,
        "object_type": MetaTextEvent,
    },
    0x03: {
        "function": chunk_name,
        "object_type": MetaTextEvent
    },
    0x04: {
        "function": instrument_name,
        "object_type": MetaTextEvent
    },
    0x05: {
        "function": lyric,
        "object_type": MetaTextEvent
    },
    0x06: {
        "function": marker,
        "object_type": MetaTextEvent
    },
    0x07: {
        "function": cue_point,
        "object_type": MetaTextEvent
    },
    0x2F: {
        "function": channel_prefix,
        "object_type": MetaChannelPrefix
    },
    0x51: {
        "function": set_tempo,
        "object_type": MetaSetTempo
    },
    0x54: {
        "function": smpte_offset,
        "object_type": MetaSMPTEOffset
    },
    0x58: {
        "function": time_signature,
        "object_type": MetaTimeSignature
    },
    0x59: {
        "function": key_signature,
        "object_type": MetaKeySignature
    }
}

MetaEventType = Union[MetaTextEvent, MetaSequenceNumber, MetaTimeSignature, MetaKeySignature, MetaSMPTEOffset,
                      MetaSetTempo, MetaChannelPrefix]
