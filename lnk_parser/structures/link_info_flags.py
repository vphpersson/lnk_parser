from enum import IntFlag
from msdsalgs.utils import Mask


class LinkInfoFlags(IntFlag):
    VolumeIDAndLocalBasePath = 0b00000000000000000000000000000001
    CommonNetworkRelativeLinkAndPathSuffix = 0b00000000000000000000000000000010


LinkInfoFlagsMask = Mask.make_class(int_flag_class=LinkInfoFlags)
