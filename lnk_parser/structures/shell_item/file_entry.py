from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, FrozenSet, ByteString
from struct import unpack_from as struct_unpack_from
from datetime import datetime, timedelta

from msdsalgs.fscc.file_attributes import FileAttributes
from msdsalgs.time import dos_date_to_datetime, dos_time_to_timedelta
from string_utils_py import underline

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.file_entry_shell_item_flags import FileEntryShellItemFlagsMask
from lnk_parser.structures.file_entry_extension_block import FileEntryExtensionBlock
from lnk_parser.utils import _decode_null_terminated_string, _format_str


@ShellItem.register_shell_item
@dataclass
class FileEntryShellItem(ShellItem):
    CLASS_TYPE_INDICATOR: ClassVar[FrozenSet[int]] = frozenset(range(0x30, 0x3f + 1))

    flags: FileEntryShellItemFlagsMask
    file_size: int | None
    last_modified_date: datetime | None
    last_modified_time: timedelta
    file_attributes: FileAttributes
    primary_name: str
    extension_block: FileEntryExtensionBlock | bytes

    @classmethod
    def _from_bytes(
        cls,
        data: ByteString | memoryview,
        base_offset: int = 0,
        system_default_encoding: str | None = None
    ) -> FileEntryShellItem:
        """
        Make a file entry shell item from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the file entry shell item.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :param system_default_encoding: The default encoding on the system on which the data was generated.
        :return: A file entry shell item.
        """

        data = memoryview(data)

        offset = base_offset

        size: int = struct_unpack_from('<H', buffer=data, offset=offset)[0]
        offset += 2

        flags = FileEntryShellItemFlagsMask.from_int(value=data[base_offset + 2] & 0x7)
        offset += 2

        file_size: int | None = struct_unpack_from('<I', buffer=data, offset=offset)[0] or None
        offset += 4

        last_modified_date: datetime = dos_date_to_datetime(dos_date=struct_unpack_from('<H', buffer=data, offset=8)[0])
        offset += 2

        last_modified_time: timedelta = dos_time_to_timedelta(
            dos_time=struct_unpack_from('<H', buffer=data, offset=10)[0]
        )
        offset += 2

        file_attributes = FileAttributes.from_int(
            value=struct_unpack_from('<H', buffer=data, offset=base_offset + 12)[0]
        )
        offset += 2

        primary_name, primary_name_byte_len = _decode_null_terminated_string(
            data=data,
            is_unicode=flags.has_unicode_strings,
            offset=offset
        )

        offset += primary_name_byte_len + 1
        offset = offset + (-offset % 2)

        extension_block_bytes = data[offset:size]

        return cls(
            flags=flags,
            file_size=file_size,
            last_modified_date=last_modified_date,
            last_modified_time=last_modified_time,
            file_attributes=file_attributes,
            primary_name=primary_name,
            extension_block=FileEntryExtensionBlock.from_bytes(data=extension_block_bytes) or extension_block_bytes
        )

    @property
    def last_modified_datetime(self) -> datetime | None:
        return (self.last_modified_date + self.last_modified_time) if self.last_modified_date else None

    def __str__(self) -> str:
        return _format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'Primary name: {self.primary_name}\n'
                f'Flags: {self.flags}\n'
                f'File size: {self.file_size}\n'
                f'File attributes: {self.file_attributes}\n'
                f'Last modified: {self.last_modified_datetime}\n'
                f'{underline(string="Extension block", underline_character="-")}\n'
                f'{self.extension_block}'
                f''
            )
        )
