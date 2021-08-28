from __future__ import annotations
from dataclasses import dataclass, field
from typing import ByteString, Optional
from uuid import UUID
from struct import unpack_from

from lnk_parser.structures.serialized_property_value import SerializedPropertyValue, STRING_NAME_GUID
from lnk_parser.structures.serialized_property_value.serialized_property_value_integer_name import \
    SerializedPropertyValueIntegerName
from lnk_parser.utils import _format_str


@dataclass
class PropertyStorage:
    storage_size: int
    version: bytes
    format_id: UUID
    properties: list[SerializedPropertyValue] = field(default_factory=list)

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0) -> Optional[PropertyStorage]:
        """
        Construct a `PropertyStorage` instance from a byte string.

        :param data: A byte string from which to construct a `PropertyStorage` instance.
        :param base_offset: The offset in the byte string from where to start reading the bytes constituting the
            `PropertyStorage` instance
        :return: A `PropertyStorage` instance or `None` if `Storage Size` indicates termination.
        """

        data = memoryview(data)[base_offset:]
        offset = 0

        storage_size: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        if storage_size == 0:
            return None

        version = bytes(data[offset:offset+4])
        offset += 4

        format_id = UUID(bytes_le=bytes(data[offset:offset+16]))
        offset += 16

        property_entries: list[SerializedPropertyValue] = []
        while True:
            if format_id == STRING_NAME_GUID:
                property_entry = None
                raise NotImplementedError
            else:
                property_entry = SerializedPropertyValueIntegerName.from_bytes(
                    data=data,
                    base_offset=offset
                )

            if property_entry is None:
                offset += 4
                break
            else:
                offset += len(property_entry)

            property_entries.append(property_entry)

        return cls(
            storage_size=storage_size,
            version=version,
            format_id=format_id,
            properties=property_entries
        )

    def __str__(self) -> str:
        properties_string: str = '\n'.join(str(property_entry) for property_entry in self.properties)

        return _format_str(
            string=(
                f'Storage size: {self.storage_size}\n'
                f'Version: {self.version}\n'
                f'Format ID: {self.format_id}\n'
                f'{properties_string}'
            )
        )
