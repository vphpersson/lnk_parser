from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Type, Optional
from abc import ABC, abstractmethod
from struct import unpack_from as struct_unpack_from, pack as struct_pack

from lnk_parser.exceptions import IncorrectExtraDataSignatureError, IncorrectExtraDataBlockSizeError
from lnk_parser.utils import _format_str


@dataclass
class ExtraData(ABC):
    SIGNATURE: ClassVar[int] = NotImplemented
    BLOCK_SIZE: ClassVar[int] = NotImplemented

    SIGNATURE_TO_EXTRA_DATA_CLASS: ClassVar[dict[int, Type[ExtraData]]] = {}

    @classmethod
    def register_extra_data(cls, extra_data_class: Type[ExtraData]) -> Type[ExtraData]:
        cls.SIGNATURE_TO_EXTRA_DATA_CLASS[extra_data_class.SIGNATURE] = extra_data_class
        return extra_data_class

    @classmethod
    @abstractmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> ExtraData:
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> Optional[ExtraData]:

        from lnk_parser.structures.extra_data.special_folder_data_block import SpecialFolderDataBlock
        from lnk_parser.structures.extra_data.tracker_data_block import TrackerDataBlock
        from lnk_parser.structures.extra_data.known_folder_data_block import KnownFolderDataBlock
        from lnk_parser.structures.extra_data.property_store_data_block import PropertyStoreDataBlock

        # The `TerminalBlock` has been reached.
        if 0 <= struct_unpack_from('<I', buffer=data, offset=base_offset)[0] < 4:
            return None

        signature: int = struct_unpack_from('<I', buffer=data, offset=base_offset+4)[0]

        if cls != ExtraData:
            if signature != cls.SIGNATURE:
                raise IncorrectExtraDataSignatureError(
                    observed_signature=signature,
                    expected_signature=cls.SIGNATURE,
                    class_name=cls.__name__
                )

            if strict and (block_size := struct_unpack_from('<I', buffer=data, offset=base_offset)[0]) != cls.BLOCK_SIZE:
                raise IncorrectExtraDataBlockSizeError(
                    observed_block_size=block_size,
                    expected_block_size=cls.BLOCK_SIZE,
                    class_name=cls.__name__
                )

            return cls._from_bytes(data=data, base_offset=base_offset, strict=strict)
        else:
            return cls.SIGNATURE_TO_EXTRA_DATA_CLASS[signature]._from_bytes(
                data=data,
                base_offset=base_offset,
                strict=strict
            )

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


@dataclass
class UnsupportedExtraData(ExtraData):
    signature: int
    block_size: int

    def __str__(self) -> str:
        return _format_str(
            string=(
                f'Type: {self.__class__.__name__}\n'
                f'Signature: 0x{struct_pack(">I", self.signature).hex()}\n'
                f'Block size: {self.block_size}'
            )
        )

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> UnsupportedExtraData:
        return cls(
            signature=struct_unpack_from('<I', buffer=data, offset=base_offset+4)[0],
            block_size=struct_unpack_from('<I', buffer=data, offset=base_offset)[0]
        )

    @classmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> ExtraData:
        pass
