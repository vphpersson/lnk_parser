from __future__ import annotations
from dataclasses import dataclass
from typing import ByteString
from struct import unpack_from
from uuid import UUID

from msdsalgs.time import filetime_to_datetime

from lnk_parser.utils import _decode_null_terminated_string, _format_str
from lnk_parser.structures.serialized_property_value import SerializedPropertyValue


@dataclass
class SerializedPropertyValueIntegerName(SerializedPropertyValue):
    property_id: int
    value_type: int
    value: bytes | str | int | UUID

    @classmethod
    def from_bytes(cls, data: ByteString | memoryview, base_offset: int = 0) -> SerializedPropertyValue | None:
        data = memoryview(data)[base_offset:]
        offset = 0

        value_size = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        if value_size == 0:
            return None

        property_id: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        # One byte offset
        offset += 1

        value_type = unpack_from('<H', buffer=data, offset=offset)[0]
        offset += 2

        # Two bytes padding
        offset += 2

        value_bytes = bytes(data[offset:offset+value_size-13])

        # TODO: Put the value types in an `IntEnum`. Refactor this.

        # TODO: More types are listed at
        #  https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-oleps/f122b9d7-e5cf-4484-8466-83f6fd94b3cc
        #  Observed: 0x40 (FILETIME), 0x15 (8-byte unsigned integer)

        # LPWSTR
        if value_type == 0x001F:
            value, _ = _decode_null_terminated_string(data=value_bytes, is_unicode=True, offset=4)
        # FILETIME
        elif value_type == 0x0040:
            value = filetime_to_datetime(filetime=value_bytes)
        # GUID
        elif value_type == 0x0048:
            value = UUID(bytes_le=value_bytes)
        else:
            value = value_bytes

        return cls(value_size=value_size, property_id=property_id, value_type=value_type, value=value)

    def __len__(self) -> int:
        return self.value_size

    def __str__(self) -> str:
        return _format_str(
            string=(
                # f'Value size: {self.value_size}\n'
                f'Value ID: {self.property_id}\n'
                f'Value type: 0x{self.value_type:02x}\n'
                f'Value: {self.value}\n'
            )
        )
