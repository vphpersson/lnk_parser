from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import ClassVar, Set, Optional
from struct import unpack_from as struct_unpack_from


@dataclass
class ShellItem(ABC):
    CLASS_TYPE_INDICATOR: ClassVar[Set[int]] = NotImplemented

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> Optional[ShellItem]:

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]
        if size == 0:
            raise ValueError

        class_type_indicator: int = data[base_offset+2]

        # TODO: Use "register pattern".
        for subclass in cls.__subclasses__():
            if class_type_indicator in subclass.CLASS_TYPE_INDICATOR:
                return subclass.from_bytes(data=data, base_offset=base_offset)

        return None
