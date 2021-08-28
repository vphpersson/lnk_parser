from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.extra_data import ExtraData
from lnk_parser.utils import _format_str


@ExtraData.register_extra_data
@dataclass
class SpecialFolderDataBlock(ExtraData):
    BLOCK_SIZE: ClassVar[int] = 0x00000010
    SIGNATURE: ClassVar[int] = 0xA0000005

    special_folder_id: int
    item_id_offset: int

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> SpecialFolderDataBlock:
        return cls(
            special_folder_id=struct_unpack_from('<I', buffer=data, offset=base_offset+8)[0],
            item_id_offset=struct_unpack_from('<I', buffer=data, offset=base_offset+12)[0]
        )

    def __str__(self) -> str:
        return _format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'Special folder ID: {self.special_folder_id}\n'
                f'Item ID offset: {self.item_id_offset}'
            )
        )
