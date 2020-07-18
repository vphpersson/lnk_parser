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
        """
        Make a shell item from a sequence of bytes.

        The concrete class is chosen based on the class type indicator field, found at a static offset in the byte
        sequence.

        :param data: A byte sequence from which to extract the bytes constituting the shell item.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A shell item.
        """

        size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]
        if size == 0:
            raise ValueError

        class_type_indicator: int = data[base_offset + 2]

        # TODO: Use the "register pattern".
        for subclass in cls.__subclasses__():
            if class_type_indicator in subclass.CLASS_TYPE_INDICATOR:
                return subclass.from_bytes(data=data, base_offset=base_offset)

        return None
