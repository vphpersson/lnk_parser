from __future__ import annotations
from dataclasses import dataclass
from typing import ByteString, ClassVar
from struct import unpack_from


@dataclass
class NTFSFileReference:
    SIZE: ClassVar[int] = 8

    mft_entry_index: bytes
    sequence_number: int

    @classmethod
    def from_bytes(cls, data: ByteString | memoryview, offset: int = 0) -> NTFSFileReference | None:
        if data[offset:offset+8] == bytes(8):
            return None

        return cls(
            mft_entry_index=bytes(data[offset:offset+6]),
            sequence_number=unpack_from('<H', buffer=data, offset=offset + 6)[0]
        )

    def __len__(self) -> int:
        return self.SIZE

    def __str__(self) -> str:
        return (
            f'MFT Entry index: {self.mft_entry_index}\n'
            f'Sequence number: {self.sequence_number}\n'
        )
