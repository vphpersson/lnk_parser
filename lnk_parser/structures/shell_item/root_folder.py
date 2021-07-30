from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, FrozenSet
from uuid import UUID
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.shell_item import ShellItem


@ShellItem.register_shell_item
@dataclass
class RootFolderShellItem(ShellItem):
    CLASS_TYPE_INDICATOR: ClassVar[FrozenSet[int]] = frozenset((0x1f,))

    sort_index: int
    # TODO: Support mapping to entities (My Computer e.g.)?
    shell_folder_identifier: UUID
    extension_block: bytes

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0) -> RootFolderShellItem:
        """
        Make a root folder shell item from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the root folder shell item.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A root folder shell item.
        """

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        return cls(
            sort_index=data[base_offset + 3],
            shell_folder_identifier=UUID(bytes_le=data[base_offset + 4:base_offset + 20]),
            extension_block=data[base_offset + 20:base_offset + size]
        )

    def __str__(self):
        return self._format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'Sort index: {self.sort_index}\n'
                f'Shell folder identifier: {self.shell_folder_identifier}'
            )
        )
