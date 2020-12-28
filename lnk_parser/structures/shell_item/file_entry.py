from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, FrozenSet, Optional
from struct import unpack_from as struct_unpack_from
from datetime import datetime, timedelta
from re import sub as re_sub

from msdsalgs.fscc.file_attributes import FileAttributes
from msdsalgs.time import dos_date_to_datetime, dos_time_to_timedelta

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.file_entry_shell_item_flags import FileEntryShellItemFlagsMask
from lnk_parser.utils import _read_null_terminated_string


@ShellItem.register_shell_item
@dataclass
class FileEntryShellItem(ShellItem):
    CLASS_TYPE_INDICATOR: ClassVar[FrozenSet[int]] = frozenset(range(0x30, 0x3f + 1))

    flags: FileEntryShellItemFlagsMask
    file_size: Optional[int]
    last_modified_time: timedelta
    last_modified_date: Optional[datetime]
    file_attributes: FileAttributes
    primary_name: str
    # extension_block: FileEntryExtensionBlock
    extension_block_bytes: bytes

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0) -> FileEntryShellItem:
        """
        Make a file entry shell item from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the file entry shell item.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A file entry shell item.
        """

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        flags = FileEntryShellItemFlagsMask.from_int(value=data[base_offset + 2] & 0x7)

        primary_name, primary_name_byte_len = _read_null_terminated_string(
            data=data,
            is_unicode=flags.has_unicode_strings,
            offset=base_offset + 14
        )

        return cls(
            flags=flags,
            file_size=struct_unpack_from('<I', buffer=data, offset=base_offset + 4)[0] or None,
            last_modified_time=dos_time_to_timedelta(dos_time=struct_unpack_from('<H', buffer=data, offset=8)[0]),
            last_modified_date=dos_date_to_datetime(dos_date=struct_unpack_from('<H', buffer=data, offset=10)[0]),
            file_attributes=FileAttributes.from_int(
                value=struct_unpack_from('<H', buffer=data, offset=base_offset + 12)[0]
            ),
            primary_name=primary_name,
            extension_block_bytes=data[base_offset + 12 + primary_name_byte_len + 1:size]
        )

    @property
    def last_modified_datetime(self) -> Optional[datetime]:
        return (self.last_modified_date + self.last_modified_time) if self.last_modified_date else None

    def __str__(self) -> str:
        return re_sub(
            pattern=r'\s+$',
            repl='',
            string=(
                f'Primary name: {self.primary_name}\n'
                f'File attritbutes: {self.file_attributes}\n'
                + (f'File size: {self.file_size}\n' if self.file_size else '')
                + (f'Last modified: {self.last_modified_time}' if self.last_modified_time else '')
            )
        )
