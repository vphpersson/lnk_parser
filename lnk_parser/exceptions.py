from typing import FrozenSet

from pyutils.my_exceptions import ParsingError


class ClassTypeIndicatorMismatchError(ParsingError):
    def __init__(self, observed_class_type_indicator: int, expected_class_type_indicators: FrozenSet[int]):
        super().__init__(
            message_header='Class type indicator mismatch.',
            observed_value=observed_class_type_indicator,
            expected_value=expected_class_type_indicators,
            expected_label=f'Expected any of'
        )


class MissingTerminalIDError(ParsingError):
    def __init__(self, observed_terminal_id: bytes, expected_terminal_id: bytes):
        super().__init__(
            message_header='Missing terminal ID.',
            observed_value=observed_terminal_id.hex(),
            expected_value=expected_terminal_id.hex(),
        )


class IncorrectExtraDataBlockSizeError(ParsingError):
    def __init__(self, observed_block_size: int, expected_block_size: int, class_name: str):
        super().__init__(
            message_header=f'Bad block size value for class {class_name}.',
            observed_value=hex(observed_block_size),
            expected_value=hex(expected_block_size),
        )


class IncorrectExtraDataSignatureError(ParsingError):
    def __init__(self, observed_signature: int, expected_signature: int, class_name: str):
        super().__init__(
            message_header=f'Bad signature value for class {class_name}',
            observed_value=hex(observed_signature),
            expected_value=hex(expected_signature),
        )


class IncorrectTrackerDataBlockLengthError(ParsingError):
    def __init__(self, observed_length: int, expected_length: int):
        super().__init__(
            message_header=f'Bad TrackerDataBlock length.',
            observed_value=observed_length,
            expected_value=expected_length,
        )


class IncorrectTrackerDataBlockVersionError(ParsingError):
    def __init__(self, observed_version: int, expected_version: int):
        super().__init__(
            message_header=f'Bad TrackerDataBlock version.',
            expected_value=expected_version,
            observed_value=observed_version
        )
