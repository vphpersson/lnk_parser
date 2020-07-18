from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Optional
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.extension_version import ExtensionVersion


@dataclass
class FileEntryExtensionBlock:

    SIGNATURE: ClassVar[int] = 0xbeef0004

    extension_version: ExtensionVersion
    creation_time: bytes
    last_accessed_time: bytes

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> Optional[FileEntryExtensionBlock]:

        size = struct_unpack_from('<H', buffer=data, offset=base_offset)
        if size == 0:
            return None