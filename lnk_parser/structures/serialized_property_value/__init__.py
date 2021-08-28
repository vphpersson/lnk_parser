from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Final
from uuid import UUID

STRING_NAME_GUID: Final[UUID] = UUID('D5CDD505-2E9C-101B-9397-08002B2CF9AE')


@dataclass
class SerializedPropertyValue(ABC):
    value_size: int

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError
