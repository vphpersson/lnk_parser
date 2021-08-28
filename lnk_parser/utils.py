from struct import unpack_from as struct_unpack_from
from typing import ByteString
from re import sub as re_sub

from pyutils.my_string import text_align_delimiter


def _read_string_data_field(buffer: ByteString, is_unicode: bool, offset: int = 0) -> tuple[str, int]:
    """
    Read a string data field.

    :param buffer: The buffer from where to read the string.
    :param is_unicode: Whether the string is unicode encoded.
    :param offset: The starting offset of the string.
    :return: The string extracted from the buffer and byte size of the string length specifier and the string.
    """

    buffer = memoryview(buffer)[offset:]

    str_len: int = struct_unpack_from('<H', buffer=buffer)[0] * (2 if is_unicode else 1)
    return (
        bytes(buffer[2:2+str_len]).decode(encoding=('utf-16-le' if is_unicode else 'ascii')),
        2 + str_len
    )


def _read_null_terminated_string(data: bytes, is_unicode: bool, offset: int = 0) -> tuple[str, int]:
    # Not sure if this is a very nice way.
    if is_unicode:
        num_string_bytes = data[offset:].index(b'\x00\x00') + 1
    else:
        num_string_bytes = data[offset:].index(b'\x00')

    return (
        data[offset:offset + num_string_bytes].decode(encoding=('utf-16-le' if is_unicode else 'ascii')),
        num_string_bytes
    )


def _format_str(string: str) -> str:
    return text_align_delimiter(
        text=re_sub(
            pattern=r'\s+$',
            repl='',
            string=string,
        ),
        delimiter=': '
    )
