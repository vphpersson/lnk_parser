from __future__ import annotations
from struct import unpack_from as struct_unpack_from
from typing import List, Optional
from pathlib import PureWindowsPath

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.shell_item.volume import VolumeShellItem
from lnk_parser.structures.shell_item.file_entry import FileEntryShellItem


class LinkTargetIDList(list):

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> LinkTargetIDList:
        id_list_size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        # TODO: Only need one list.
        data_list: List[bytes] = []

        offset = base_offset + 0x2
        read_data = 0
        while (read_data + 2) < id_list_size:
            item_id_size: int = struct_unpack_from('<H', buffer=data, offset=offset)[0]
            data_list.append(data[offset:offset+item_id_size])

            offset += item_id_size
            read_data += item_id_size

        return cls(ShellItem.from_bytes(data=d) for d in data_list)

    @property
    def path(self) -> Optional[PureWindowsPath]:
        path_segments: List[str] = []
        for link_target in self.__iter__():
            if isinstance(link_target, VolumeShellItem):
                if link_target.name:
                    path_segments.append(link_target.name)
            elif isinstance(link_target, FileEntryShellItem):
                path_segments.append(link_target.primary_name)

        if not path_segments:
            return None

        return PureWindowsPath(*path_segments)
