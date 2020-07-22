from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Set, Optional, Dict, Type
from struct import unpack_from as struct_unpack_from

from lnk_parser.exceptions import ClassTypeIndicatorMismatchError


@dataclass
class ShellItem(ABC):
    CLASS_TYPE_INDICATOR: ClassVar[Set[int]] = NotImplemented

    CLASS_TYPE_INDICATOR_TO_SHELL_ITEM_CLASS: ClassVar[Dict[int, Type[ShellItem]]] = {}

    @classmethod
    def register_shell_item(cls, shell_item_class: Type[ShellItem]) -> Type[ShellItem]:
        for class_type_indicator in shell_item_class.CLASS_TYPE_INDICATOR:
            cls.CLASS_TYPE_INDICATOR_TO_SHELL_ITEM_CLASS[class_type_indicator] = shell_item_class
        return shell_item_class

    # TODO: Add `strict` parameter.
    @classmethod
    @abstractmethod
    def _from_bytes(cls, data: bytes, base_offset: int = 0) -> ShellItem:
        raise NotImplementedError

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

        if cls != ShellItem:
            if class_type_indicator not in cls.CLASS_TYPE_INDICATOR:
                raise ClassTypeIndicatorMismatchError(
                    observed_class_type_indicator=class_type_indicator,
                    expected_class_type_indicators=cls.CLASS_TYPE_INDICATOR
                )
            return cls._from_bytes(
                data=data,
                base_offset=base_offset
            )
        else:
            return cls.CLASS_TYPE_INDICATOR_TO_SHELL_ITEM_CLASS[class_type_indicator]._from_bytes(
                data=data,
                base_offset=base_offset
            )
