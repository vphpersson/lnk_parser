from logging import Logger, getLogger
from struct import unpack_from as struct_unpack_from
from typing import ByteString
from re import sub as re_sub
from locale import getpreferredencoding

from string_utils_py import text_align_delimiter


LOG: Logger = getLogger(__name__)


def get_system_default_encoding(*args, **kwargs) -> str:
    """
    Return the current system's default encoding.

    :param args: Arguments to be passed to `locale.getpreferredencoding`.
    :param kwargs: Keyword arguments to be passed to `locale.getpreferredencoding`.
    :return: The current system's default encoding.
    """
    
    return res[1] if isinstance(res := getpreferredencoding(*args, **kwargs), tuple) else res


def _decode_string_data_field(
    buffer: ByteString | memoryview,
    is_unicode: bool,
    offset: int = 0,
    system_default_encoding: str | None = None
) -> tuple[str, int]:
    """
    Read a string data field.

    :param buffer: The buffer from where to read the string.
    :param is_unicode: Whether the string is unicode encoded.
    :param offset: The starting offset of the string.
    :param system_default_encoding: The default encoding on the system which produced the null-terminated string bytes.
        Necessary to know when not Unicode-encoded. Defaults to the current system's default encoding.
    :return: The string extracted from the buffer and byte size of the string length specifier and the string.
    """

    buffer = memoryview(buffer)[offset:]

    encoding = 'utf-16-le' if is_unicode else system_default_encoding or get_system_default_encoding()

    str_len: int = struct_unpack_from('<H', buffer=buffer)[0] * (2 if is_unicode else 1)
    return bytes(buffer[2:2+str_len]).decode(encoding=encoding), 2 + str_len


def _decode_null_terminated_string(
    data: ByteString | memoryview,
    is_unicode: bool,
    offset: int = 0,
    system_default_encoding: str | None = None
) -> tuple[str, int]:
    """
    Decode a null-terminated string from a data buffer.

    :param data: The data from which to decode a null-terminated string.
    :param is_unicode: Whether the string is Unicode-encoded.
    :param offset: The offset into the data buffer from where to start reading the null-terminated string.
    :param system_default_encoding: The default encoding on the system which produced the null-terminated string bytes.
        Necessary to know when not Unicode-encoded. Defaults to the current system's default encoding.
    :return: The decoded string and the number of bytes it constituted in the data buffer.
    """

    # NOTE: Not sure if this is a very nice way of decoding.

    if is_unicode:
        encoding = 'utf-16-le'

        num_string_bytes = bytes(data[offset:]).index(b'\x00\x00') + 1
        if num_string_bytes == 1:
            return '', num_string_bytes

        string_bytes = bytes(data[offset:offset + num_string_bytes])

        try:
            return string_bytes.decode(encoding=encoding), num_string_bytes
        except UnicodeError as e:
            raise ValueError(
                f'Unable to decode the bytes {string_bytes} with the encoding {encoding}. '
                'Maybe the offset is incorrect.'
            ) from e
    else:
        system_default_encoding = system_default_encoding or get_system_default_encoding()
        num_string_bytes = bytes(data[offset:]).index(b'\x00')
        string_bytes = bytes(data[offset:offset + num_string_bytes])

        try:
            return string_bytes.decode(encoding=system_default_encoding), num_string_bytes
        except UnicodeError as e:
            raise ValueError(
                f'Unable to decode the bytes {string_bytes} with the system encoding {system_default_encoding}. '
                'Maybe the encoding or offset is incorrect.'
            ) from e


def _format_str(string: str) -> str:
    return text_align_delimiter(
        text=re_sub(
            pattern=r'\s+$',
            repl='',
            string=string,
        ),
        delimiter=': '
    )
