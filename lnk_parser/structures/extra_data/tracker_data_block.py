from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Tuple
from struct import unpack_from as struct_unpack_from
from uuid import UUID

from lnk_parser.structures.extra_data import ExtraData
from lnk_parser.exceptions import IncorrectTrackerDataBlockLengthError, IncorrectTrackerDataBlockVersionError


@ExtraData.register_extra_data
@dataclass
class TrackerDataBlock(ExtraData):
    BLOCK_SIZE: ClassVar[int] = 0x00000060
    SIGNATURE: ClassVar[int] = 0xA0000003

    LENGTH: ClassVar[int] = 0x00000058
    VERSION: ClassVar[int] = 0x00000000

    machine_id: str
    droid: Tuple[UUID, UUID]
    droid_birth: Tuple[UUID, UUID]

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> TrackerDataBlock:

        if strict:
            if (length := struct_unpack_from('<I', buffer=data, offset=base_offset+8)[0]) != cls.LENGTH:
                raise IncorrectTrackerDataBlockLengthError(observed_length=length, expected_length=cls.LENGTH)

            if (version := struct_unpack_from('<I', buffer=data, offset=base_offset+12)[0]) != cls.VERSION:
                raise IncorrectTrackerDataBlockVersionError(observed_version=version, expected_version=cls.VERSION)

        return cls(
            machine_id=data[base_offset+16:base_offset+32].decode(encoding='ascii').replace('\x00', ''),
            droid=(
                UUID(bytes_le=data[base_offset+32:base_offset+48]),
                UUID(bytes_le=data[base_offset+48:base_offset+64])
            ),
            droid_birth=(
                UUID(bytes_le=data[base_offset+64:base_offset+80]),
                UUID(bytes_le=data[base_offset+80:base_offset+96])
            )
        )
