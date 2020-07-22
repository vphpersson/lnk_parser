from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Type, Dict
from abc import ABC, abstractmethod
from struct import unpack_from as struct_unpack_from

from lnk_parser.exceptions import IncorrectExtraDataSignatureError, IncorrectExtraDataBlockSizeError


@dataclass
class ExtraData(ABC):
    SIGNATURE: ClassVar[int] = NotImplemented
    BLOCK_SIZE: ClassVar[int] = NotImplemented

    SIGNATURE_TO_EXTRA_DATA_CLASS: ClassVar[Dict[int, Type[ExtraData]]] = {}

    @classmethod
    def register_extra_data(cls, extra_data_class: Type[ExtraData]) -> Type[ExtraData]:
        cls.SIGNATURE_TO_EXTRA_DATA_CLASS[extra_data_class.SIGNATURE] = extra_data_class
        return extra_data_class

    @classmethod
    @abstractmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> ExtraData:
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0, strict: bool = True) -> ExtraData:

        from lnk_parser.structures.extra_data.special_folder_data_block import SpecialFolderDataBlock
        from lnk_parser.structures.extra_data.tracker_data_block import TrackerDataBlock

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
