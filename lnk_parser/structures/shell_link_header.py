from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, ByteString
from struct import unpack_from as struct_unpack_from
from uuid import UUID
from datetime import datetime
from re import sub as re_sub

from msdsalgs.fscc.file_attributes import FileAttributes
from msdsalgs.time import filetime_to_datetime
from string_utils_py import text_align_delimiter

from lnk_parser.structures.link_flags import LinkFlagsMask
from lnk_parser.structures.show_command import ShowCommand
from lnk_parser.structures.hot_keys_flags import HotKeyFlags


@dataclass
class ShellLinkHeader:
    SIZE: ClassVar[int] = 0x0000004C
    LINK_CLSID: ClassVar[UUID] = UUID('00021401-0000-0000-C000-000000000046')

    link_flags: LinkFlagsMask
    file_attributes: FileAttributes
    creation_time: datetime | None
    access_time: datetime | None
    write_time: datetime | None
    file_size: int
    icon_index: int
    show_command: ShowCommand
    hot_key: HotKeyFlags | None

    @classmethod
    def from_bytes(cls, data: ByteString | memoryview, base_offset: int = 0) -> ShellLinkHeader:
        """
        Make a shell link header from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the shell link header.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A shell link header.
        """

        data = memoryview(data)

        # TODO: Remove magic numbers?

        hot_key = HotKeyFlags.from_bytes(data=data[base_offset+0x0040:0x0042])

        return cls(
            link_flags=LinkFlagsMask.from_int(value=struct_unpack_from('<I', buffer=data, offset=base_offset + 0x0014)[0]),
            file_attributes=FileAttributes.from_int(
                value=struct_unpack_from('<I', buffer=data, offset=base_offset+0x0018)[0]
            ),
            creation_time=filetime_to_datetime(filetime=data[base_offset+0x001C:base_offset+0x0024]),
            access_time=filetime_to_datetime(filetime=data[base_offset+0x0024:base_offset+0x002C]),
            write_time=filetime_to_datetime(filetime=data[base_offset+0x002C:base_offset+0x0034]),
            file_size=struct_unpack_from('<I', buffer=data, offset=base_offset+0x0034)[0],
            icon_index=struct_unpack_from('<I', buffer=data, offset=base_offset+0x0038)[0],
            show_command=ShowCommand(struct_unpack_from('<I', buffer=data, offset=base_offset+0x003C)[0]),
            hot_key=hot_key if hot_key.key else None
        )

    def __len__(self) -> int:
        return self.SIZE

    def __str__(self) -> str:
        return text_align_delimiter(
            text=re_sub(
                pattern=r'\s+$',
                repl='',
                string=(
                    f'Link flags: {self.link_flags}\n'
                    f'File attributes: {self.file_attributes}\n'
                    f'Creation time: {self.creation_time}\n'
                    f'Access time: {self.access_time}\n'
                    f'Write time: {self.write_time}\n'
                    f'File size: {self.file_size}\n'
                    f'Icon index: {self.icon_index}\n'
                    f'Show command: {self.show_command.name}\n'
                    f'Hot key: {self.hot_key}\n'
                )
            ),
            delimiter=':'
        )
