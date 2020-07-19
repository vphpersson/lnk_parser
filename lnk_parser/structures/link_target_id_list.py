from __future__ import annotations
from struct import unpack_from as struct_unpack_from
from typing import List, Optional
from pathlib import PureWindowsPath

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.shell_item.volume import VolumeShellItem
from lnk_parser.structures.shell_item.file_entry import FileEntryShellItem


class LinkTargetIDList(list):

    TERMINAL_ID = b'\x00\x00'

    # TODO: Add a `strict` keyword argument (here and elsewhere)
    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> LinkTargetIDList:
        """
        Make a link target id list from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the link target id list.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A link target id list.
        """
        
        id_list_size: int = struct_unpack_from('<H', buffer=data, offset=base_offset)[0]

        # TODO: Only need one list. But make this nicer overall first!
        data_list: List[bytes] = []

        offset = base_offset + 0x2
        read_data = 0
        while (read_data + 2) < id_list_size:
            item_id_size: int = struct_unpack_from('<H', buffer=data, offset=offset)[0]
            data_list.append(data[offset:offset+item_id_size])

            offset += item_id_size
            read_data += item_id_size

        return cls(ShellItem.from_bytes(data=d, base_offset=0) for d in data_list)

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
