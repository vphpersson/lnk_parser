from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Set, Optional
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.volume_shell_item_flags import VolumeShellItemFlagsMask


@dataclass
class VolumeShellItem(ShellItem):
    CLASS_TYPE_INDICATOR: ClassVar[Set[int]] = set(range(0x20, 0x2f + 1))

    flags: VolumeShellItemFlagsMask
    # just picking a name -- is this what the flag indicates?
    other: bytes
    name: Optional[str] = None

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> VolumeShellItem:
        """
        Make a volume shell item from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the volume shell item.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A volume shell item.
        """

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        flags = VolumeShellItemFlagsMask.from_int(value=data[base_offset + 2] & 0x7)
        other = data[base_offset + 3:size]

        return cls(
            flags=flags,
            name=other.decode(encoding='ascii').replace('\x00', '') if flags.has_name else None,
            other=other
        )

    def __str__(self) -> str:
        return f'Name: {self.name}' if self.name else ''
