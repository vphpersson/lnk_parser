from enum import IntFlag
from msdsalgs.utils import Mask


class FileEntryShellItemFlags(IntFlag):
    IS_DIRECTORY = 0x1
    IS_FILE = 0x2
    HAS_UNICODE_STRINGS = 0x4
    UNKNOWN = 0x8
    HAS_CLASS_IDENTIFIER = 0x80


FileEntryShellItemFlagsMask = Mask.make_class(int_flag_class=FileEntryShellItemFlags)
