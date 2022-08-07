from __future__ import annotations
from logging import Logger, getLogger
from dataclasses import dataclass
from typing import ClassVar, ByteString
from struct import unpack_from as struct_unpack_from
from datetime import datetime

from msdsalgs.time import dos_date_to_datetime
from string_utils_py import underline

from lnk_parser.structures.extension_version import ExtensionVersion
from lnk_parser.structures.ntfs_file_reference import NTFSFileReference
from lnk_parser.utils import _decode_null_terminated_string


LOG: Logger = getLogger(__name__)


@dataclass
class FileEntryExtensionBlock:

    SIGNATURE: ClassVar[int] = 0xbeef0004

    extension_version: ExtensionVersion
    creation_datetime: datetime
    last_access_datetime: datetime
    ntfs_file_reference: NTFSFileReference | None = None
    long_name: str | None = None
    localized_name: str | None = None
    first_extension_block_version_offset: int | None = None

    @classmethod
    def from_bytes(
        cls,
        data: ByteString | memoryview,
        base_offset: int = 0
    ) -> FileEntryExtensionBlock | None:

        data = memoryview(data)

        offset = base_offset

        if (size := struct_unpack_from('<H', buffer=data, offset=offset)[0]) == 0:
            return None
        offset += 2

        extension_version = ExtensionVersion(struct_unpack_from('<H', buffer=data, offset=offset)[0])
        offset += 2

        if (signature := struct_unpack_from('<I', buffer=data, offset=offset)[0]) != cls.SIGNATURE:
            LOG.warning(f'Unexpected file entry extension block signature: {hex(signature)}')
            return None
        offset += 4

        creation_datetime: datetime = dos_date_to_datetime(dos_date=data, offset=offset)
        offset += 4

        last_access_datetime: datetime = dos_date_to_datetime(dos_date=data, offset=offset)
        offset += 4

        # unknown
        offset += 2

        if extension_version >= ExtensionVersion.WINDOWS_VISTA:
            # unknown
            offset += 2

            ntfs_file_reference = NTFSFileReference.from_bytes(data=data, offset=offset)
            offset += len(ntfs_file_reference)

            # unknown
            offset += 8
        else:
            ntfs_file_reference = None

        if extension_version >= ExtensionVersion.WINDOWS_XP_2003:
            long_string_size = struct_unpack_from('<H', buffer=data, offset=offset)[0]
            offset += 2
        else:
            long_string_size = None

        if extension_version >= ExtensionVersion.WINDOWS_81_10:
            # unknown
            offset += 4

        if extension_version >= ExtensionVersion.WINDOWS_2008_7_80:
            # unknown
            offset += 4

        if extension_version >= ExtensionVersion.WINDOWS_XP_2003:
            long_name, num_long_name_bytes = _decode_null_terminated_string(data=data, is_unicode=True, offset=offset)
            offset += num_long_name_bytes + 1
            offset = offset + (-offset % 2)

        else:
            long_name = None

        if extension_version >= ExtensionVersion.WINDOWS_VISTA and long_string_size:
            localized_name, num_localized_name_bytes = _decode_null_terminated_string(
                data=data,
                is_unicode=True,
                offset=offset
            )
            offset += num_localized_name_bytes + 1
            offset = offset + (-offset % 2)
        elif extension_version >= ExtensionVersion.WINDOWS_XP_2003 and long_string_size:
            localized_name, num_localized_name_bytes = _decode_null_terminated_string(
                data=data,
                is_unicode=False,
                offset=offset
            )
            offset += num_localized_name_bytes + 1
            offset = offset + (-offset % 2)
        else:
            localized_name = None

        if extension_version >= ExtensionVersion.WINDOWS_XP_2003:
            first_extension_block_version_offset = struct_unpack_from('<H', buffer=data, offset=offset)[0]
        else:
            first_extension_block_version_offset = None

        return cls(
            extension_version=extension_version,
            creation_datetime=creation_datetime,
            last_access_datetime=last_access_datetime,
            ntfs_file_reference=ntfs_file_reference,
            long_name=long_name,
            localized_name=localized_name,
            first_extension_block_version_offset=first_extension_block_version_offset
        )

    def __str__(self) -> str:

        ntfs_file_reference_label = 'NTFS file reference'

        return (
            f'Extension version: {repr(self.extension_version)}\n'
            f'Creation time: {self.creation_datetime}\n'
            f'Last access time: {self.last_access_datetime}\n'
            f'{underline(string=ntfs_file_reference_label, underline_character="%")}\n'
            f'{self.ntfs_file_reference or ""}'
            f'{"%" * len(ntfs_file_reference_label)}\n'
            f'Long name: {self.long_name}\n'
            f'Localized name: {self.localized_name}\n'
            f'First ext. block ver. offset: {self.first_extension_block_version_offset}\n'
        )
