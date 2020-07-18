from struct import unpack_from as struct_unpack_from
from typing import Tuple


def _read_string_data_field(buffer: bytes, base_offset: int, is_unicode: bool) -> Tuple[str, int]:
    str_len: int = struct_unpack_from('<H', buffer=buffer, offset=base_offset)[0] * (2 if is_unicode else 1)
    return (
        buffer[base_offset + 2:base_offset + 2 + str_len].decode(encoding=('utf-16-le' if is_unicode else 'ascii')),
        2 + str_len
    )


def _read_null_terminated_string(data: bytes, is_unicode: bool, base_offset: int = 0):

    if is_unicode:
        num_string_bytes = data[base_offset:].index(b'\x00\x00') + 1 - base_offset
    else:
        num_string_bytes = data[base_offset:].index(b'\x00') - base_offset

    return data[base_offset:base_offset+num_string_bytes].decode(encoding=('utf-16-le' if is_unicode else 'ascii'))
