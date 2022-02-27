from __future__ import annotations
from dataclasses import dataclass
from typing import ByteString
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.drive_type import DriveType


@dataclass
class VolumeID:
    drive_type: DriveType
    drive_serial_number: bytes
    volume_label: str

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0) -> VolumeID:

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
            ]).decode(encoding='ascii')

        return cls(
            drive_type=DriveType(struct_unpack_from('<I', buffer=data, offset=base_offset+4)[0]),
            drive_serial_number=bytes(data[base_offset+8:base_offset+12]),
            volume_label=volume_label.replace('\x00', '')
        )
