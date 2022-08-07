from __future__ import annotations
from dataclasses import dataclass
from typing import ByteString
from struct import unpack_from


@dataclass
class NTFSFileReference:
    mft_entry_index: bytes
    sequence_number: int

    @classmethod
    def from_bytes(cls, data: ByteString | memoryview, offset: int = 0) -> NTFSFileReference:
        return cls(
            mft_entry_index=bytes(data[offset:offset+6]),
            sequence_number=unpack_from('<H', buffer=data, offset=offset + 6)[0]
        )

    def __len__(self) -> int:
        return 8

    def __str__(self) -> str:
        return (
            f'MFT Entry index: {self.mft_entry_index}\n'
            f'Sequence number: {self.sequence_number}\n'
        )
