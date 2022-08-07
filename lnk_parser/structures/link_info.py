from __future__ import annotations
from dataclasses import dataclass, InitVar
from typing import ByteString
from struct import unpack_from as struct_unpack_from

from lnk_parser.structures.volume_id import VolumeID
from lnk_parser.structures.link_info_flags import LinkInfoFlagsMask
from lnk_parser.utils import _decode_null_terminated_string


@dataclass
class LinkInfo:
    link_info_size: InitVar[int]
    link_info_flags: LinkInfoFlagsMask
    volume_id: VolumeID | None = None
    local_base_path: str | None = None
    common_network_relative_link: str | None = None
    common_path_suffix: str | None = None

    def __post_init__(self, link_info_size: int):
        self._link_info_size = link_info_size

    @property
    def size(self) -> int:
        return self._link_info_size

    @classmethod
    def from_bytes(
        cls,
        data: ByteString | memoryview,
        base_offset: int = 0,
        system_default_encoding: str | None = None
    ) -> LinkInfo:
        """
        Make a link info structure from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the link info structure.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :param system_default_encoding: The default encoding on the system on which the data was generated.
        :return: A link info structure.
        """

        data = memoryview(data)

        link_info_size: int = struct_unpack_from('<I', buffer=data, offset=base_offset)[0]

        link_info_header_size: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 4)[0]

        link_info_flags = LinkInfoFlagsMask.from_int(
            value=struct_unpack_from('<I', buffer=data, offset=base_offset + 8)[0]
        )

        volume_id_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 12)[0]

        local_base_path_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 16)[0]

        # TODO: Implement structure.
        common_network_relative_link_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 20)[0]

        common_path_suffix_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 24)[0]

        if link_info_header_size >= 0x00000024:
            local_base_path_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 28)[0]
            local_base_path_is_unicode = True

            common_path_suffix_offset: int = struct_unpack_from('<I', buffer=data, offset=base_offset + 32)[0]
            common_path_is_unicode = True
        else:
            local_base_path_is_unicode = False
            common_path_is_unicode = False

        return cls(
            link_info_size=link_info_size,
            link_info_flags=link_info_flags,
            volume_id=VolumeID.from_bytes(
                data=data,
                base_offset=base_offset + volume_id_offset,
                system_default_encoding=system_default_encoding
            ) if link_info_flags.volume_id_and_local_base_path else None,
            local_base_path=_decode_null_terminated_string(
                data=data,
                is_unicode=local_base_path_is_unicode,
                offset=base_offset + local_base_path_offset,
                system_default_encoding=system_default_encoding
            )[0] if link_info_flags.volume_id_and_local_base_path else None,
            common_path_suffix=_decode_null_terminated_string(
                data=data,
                is_unicode=common_path_is_unicode,
                offset=base_offset + common_path_suffix_offset,
                system_default_encoding=system_default_encoding
            )[0] if local_base_path_offset != 0 else None,
        )

    def __str__(self) -> str:
        return (
            f'Flags: {self.link_info_flags}\n'
            f'{self.volume_id}'
            f'Local base path: {self.local_base_path}\n'
            f'Common path suffix: {self.common_path_suffix}\n'
        )
