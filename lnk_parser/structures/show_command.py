from enum import IntEnum


class ShowCommand(IntEnum):
    SW_SHOWNORMAL = 0x00000001
    SW_SHOWMAXIMIZED = 0x00000003
    SW_SHOWMINNOACTIVE = 0x00000007
