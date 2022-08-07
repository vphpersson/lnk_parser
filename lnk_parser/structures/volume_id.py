from __future__ import annotations
from dataclasses import dataclass
from typing import ByteString
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.drive_type import DriveType
from lnk_parser.utils import get_system_default_encoding


@dataclass
class VolumeID:
    drive_type: DriveType
    drive_serial_number: bytes
    volume_label: str

    @classmethod
    def from_bytes(
        cls, data: ByteString | memoryview,
        base_offset: int = 0,
        system_default_encoding: str | None = None
    ) -> VolumeID:

        data = memoryview(data)

        volume_id_size: int = struct_unpack_from('<I', buffer=data, offset=base_offset)[0]

        volume_label_offset = struct_unpack_from('<I', buffer=data, offset=base_offset+12)[0]
        if volume_label_offset == 0x00000014:
            volume_label = bytes(data[
                base_offset+struct_unpack_from('<I', buffer=data, offset=base_offset+16)[0]:base_offset+volume_id_size
            ]).decode(encoding='utf-16-le')
        else:
            volume_label = bytes(data[
                base_offset+volume_label_offset:base_offset+volume_id_size
            ]).decode(encoding=system_default_encoding or get_system_default_encoding())

        return cls(
            drive_type=DriveType(struct_unpack_from('<I', buffer=data, offset=base_offset+4)[0]),
            drive_serial_number=bytes(data[base_offset+8:base_offset+12]),
            volume_label=volume_label.replace('\x00', '')
        )

    def __str__(self) -> str:
        return (
            f'Drive type: {repr(self.drive_type)}\n'
            f'Drive serial number: {self.drive_serial_number}\n'
            f'Volume label: {self.volume_label}\n'
        )
