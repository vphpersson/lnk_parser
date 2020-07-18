from dataclasses import dataclass, InitVar
from typing import Optional
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.volume_id import VolumeID
from lnk_parser.structures.link_flags import LinkFlagsMask
from lnk_parser.utils import _read_null_terminated_string


@dataclass
class LinkInfo:
    link_info_size: InitVar[int]
    volume_id: Optional[VolumeID] = None
    local_base_path: Optional[str] = None
    common_network_relative_link: Optional[str] = None
    common_path_suffix: Optional[str] = None

    def __post_init__(self, link_info_size: int):
        self._link_info_size = link_info_size

    @property
    def size(self):
        return self._link_info_size

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0):

        link_info_size: int = struct_unpack_from('<I', buffer=data, offset=base_offset)[0]
        link_info_header_size: int = struct_unpack_from('<I', buffer=data, offset=base_offset+4)[0]

        link_info_flags = LinkFlagsMask.from_int(value=struct_unpack_from('>I', buffer=data, offset=base_offset+8)[0])

        volume_id_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+12)[0]

        local_base_path_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+16)[0]
        local_base_path_is_unicode: bool = False

        common_network_relative_link_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+20)[0]

        common_path_suffix_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+24)[0]
        common_path_is_unicode: bool = False

        if link_info_header_size >= 0x00000024:
            local_base_path_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+28)[0]
            local_base_path_is_unicode: bool = True

        if link_info_header_size >= 0x00000024:
            common_path_suffix_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset+32)[0]
            common_path_is_unicode: bool = True

        return cls(
            link_info_size=link_info_size,
            volume_id=VolumeID.from_bytes(
                data=data,
                base_offset=volume_id_offset
            ) if link_info_flags.volume_id_and_local_base_path else None,
            local_base_path=_read_null_terminated_string(
                data=data,
                is_unicode=local_base_path_is_unicode,
                base_offset=local_base_path_offset
            ) if link_info_flags.volume_id_and_local_base_path else None,
            common_path_suffix=_read_null_terminated_string(
                data=data,
                is_unicode=common_path_is_unicode,
                base_offset=common_path_suffix_offset
            ) if local_base_path_offset != 0 else None,
        )