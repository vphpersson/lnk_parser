from enum import IntFlag
from msdsalgs.utils import Mask


class LinkFlags(IntFlag):
    HasLinkTargetIDList = 0b00000000000000000000000000000001
    HasLinkInfo = 0b00000000000000000000000000000010
    HasName = 0b00000000000000000000000000000100
    HasRelativePath = 0b00000000000000000000000000001000
    HasWorkingDir = 0b00000000000000000000000000010000
    HasArguments = 0b00000000000000000000000000100000
    HasIconLocation = 0b00000000000000000000000001000000
    IsUnicode = 0b00000000000000000000000010000000
    ForceNoLinkInfo = 0b00000000000000000000000100000000
    HasExpString = 0b00000000000000000000001000000000
    RunInSeparateProcess = 0b00000000000000000000010000000000
    Unused1 = 0b00000000000000000000100000000000
    HasDarwinID = 0b00000000000000000001000000000000
    RunAsUser = 0b00000000000000000010000000000000
    HasExpIcon = 0b00000000000000000100000000000000
    NoPidlAlias = 0b00000000000000001000000000000000
    Unused2 = 0b00000000000000010000000000000000
    RunWithShimLayer = 0b00000000000000100000000000000000
    ForceNoLinkTrack = 0b00000000000001000000000000000000
    EnableTargetMetadata = 0b00000000000010000000000000000000
    DisableLinkPathTracking = 0b00000000000100000000000000000000
    DisableKnownFolderTracking = 0b00000000001000000000000000000000
    DisableKnownFolderAlias = 0b00000000010000000000000000000000
    AllowLinkToLink = 0b00000000100000000000000000000000
    UnaliasOnSave = 0b00000001000000000000000000000000
    PreferEnvironmentPath = 0b00000010000000000000000000000000
    KeepLocalIDListForUNCTarget = 0b00000100000000000000000000000000


LinkFlagsMask = Mask.make_class(int_flag_class=LinkFlags)
