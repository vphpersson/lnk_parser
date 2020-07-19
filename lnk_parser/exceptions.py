from abc import ABC
from typing import FrozenSet


class ClassTypeIndicatorMismatchError(Exception):
    def __init__(
        self,
        observed_class_type_indicator: int,
        expected_class_type_indicators: FrozenSet[int]
    ):
        self.observed_class_type_indicator = observed_class_type_indicator
        self.expected_class_type_indicators = expected_class_type_indicators

        super().__init__(
            f'Class type indicator mismatch. '
            f'Expected any of {self.expected_class_type_indicators}. '
            f'Observed {self.observed_class_type_indicator}.'
        )


class ParsingError(Exception, ABC):
    def __init__(self, message_header: str, expected_value: bytes, observed_value: bytes):
        super().__init__(
            f'{message_header} '
            f'Expected {expected_value.hex()}. '
            f'Observed {observed_value.hex()}.'
        )


class MissingTerminalIDError(ParsingError):
    def __init__(self, observed_value: bytes, terminal_id: bytes):
        super().__init__(
            message_header='Missing terminal ID.',
            expected_value=terminal_id,
            observed_value=observed_value
        )
