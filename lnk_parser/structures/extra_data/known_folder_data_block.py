from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.extra_data import ExtraData
from lnk_parser.utils import _format_str


@ExtraData.register_extra_data
@dataclass
class KnownFolderDataBlock(ExtraData):
    BLOCK_SIZE: ClassVar[int] = 0x0000001C
    SIGNATURE: ClassVar[int] = 0xA000000B

    known_folder_id: bytes
    offset: int

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> KnownFolderDataBlock:
        return cls(
            known_folder_id=data[base_offset+8:base_offset+24],
            offset=struct_unpack_from('<I', buffer=data, offset=base_offset+24)[0]
        )

    def __str__(self) -> str:
        return _format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'Known folder ID: {self.known_folder_id.hex()}\n'
                f'Offset: {self.offset}'
            )
        )
