from enum import IntFlag
from msdsalgs.utils import Mask


class VolumeShellItemFlags(IntFlag):
    HAS_NAME = 0x1
    UNKNOWN_1 = 0x2
    UNKNOWN_2 = 0x4
    IS_REMOVABLE_MEDIA = 0x8


VolumeShellItemFlagsMask = Mask.make_class(int_flag_class=VolumeShellItemFlags)
