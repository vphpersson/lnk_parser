from struct import unpack_from as struct_unpack_from


def _read_string_data_field(buffer: bytes, is_unicode: bool, offset: int = 0) -> tuple[str, int]:
    str_len: int = struct_unpack_from('<H', buffer=buffer, offset=offset)[0] * (2 if is_unicode else 1)
    return (
        buffer[offset + 2:offset + 2 + str_len].decode(encoding=('utf-16-le' if is_unicode else 'ascii')),
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
