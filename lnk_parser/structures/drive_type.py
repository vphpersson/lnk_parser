from enum import IntEnum


class DriveType(IntEnum):
    DRIVE_UNKNOWN = 0x00000000
    DRIVE_NO_ROOT_DIR = 0x00000001
    DRIVE_REMOVABLE = 0x00000002
    DRIVE_FIXED = 0x00000003
    DRIVE_REMOTE = 0x00000004
    DRIVE_CDROM = 0x00000005
    DRIVE_RAMDISK = 0x00000006
