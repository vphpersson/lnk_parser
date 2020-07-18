from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Set
from uuid import UUID
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.shell_item import ShellItem


@dataclass
class RootFolderShellItem(ShellItem):
    CLASS_TYPE_INDICATOR: ClassVar[Set[int]] = {0x1f}

    sort_index: int
    shell_folder_identifier: UUID
    extension_block: bytes

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> RootFolderShellItem:

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        return cls(
            sort_index=data[base_offset+3],
            shell_folder_identifier=UUID(bytes_le=data[base_offset+4:base_offset+20]),
            extension_block=data[base_offset+20:base_offset+size]
        )
