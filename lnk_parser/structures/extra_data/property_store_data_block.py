from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import ClassVar

from lnk_parser.structures.extra_data import ExtraData
from lnk_parser.structures.property_storage import PropertyStorage
from lnk_parser.utils import _format_str


@ExtraData.register_extra_data
@dataclass
class PropertyStoreDataBlock(ExtraData):
    SIGNATURE: ClassVar[int] = 0xA0000009

    block_size: InitVar[int]
    property_storages: list[PropertyStorage] = field(default_factory=list)

    def __post_init__(self, block_size: int):
        self.BLOCK_SIZE = block_size

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> PropertyStoreDataBlock:

        data = memoryview(data)[base_offset:]
        offset = 0

        # Skipping block size and signature.
        offset += 8

        property_storages: list[PropertyStorage] = []
        while property_storage := PropertyStorage.from_bytes(data=data, base_offset=offset):
            property_storages.append(property_storage)
            offset += property_storage.storage_size

        return cls(
            block_size=offset,
            property_storages=property_storages
        )

    def __str__(self) -> str:

        property_storages_string: str = '\n'.join(str(property_storage) for property_storage in self.property_storages)

        return _format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'{property_storages_string}'
            )
        )
