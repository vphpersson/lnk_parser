from enum import IntFlag
from msdsalgs.utils import Mask


class LinkInfoFlags(IntFlag):
    VolumeIDAndLocalBasePath = 0b10000000000000000000000000000000
    CommonNetworkRelativeLinkAndPathSuffix = 0b01000000000000000000000000000000


LinkInfoFlagsMask = Mask.make_class(int_flag_class=LinkInfoFlags)
