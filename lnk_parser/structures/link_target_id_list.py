from __future__ import annotations
from struct import unpack_from as struct_unpack_from, calcsize as struct_calcsize
from typing import ByteString
from pathlib import PureWindowsPath

from lnk_parser.structures.shell_item import ShellItem
from lnk_parser.structures.shell_item.volume import VolumeShellItem
from lnk_parser.structures.shell_item.file_entry import FileEntryShellItem
from lnk_parser.exceptions import MissingTerminalIDError


class LinkTargetIDList(list):

    TERMINAL_ID = b'\x00\x00'

    @classmethod
    def from_bytes(
        cls,
        data: ByteString | memoryview,
        base_offset: int = 0,
        system_default_encoding: str | None = None
    ) -> LinkTargetIDList:
        """
        Make a link target id list from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the link target id list.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :param system_default_encoding: The default encoding on the system on which the data was generated.
        :return: A link target id list.
        """

        data = memoryview(data)

        id_list_size_format: str = '<H'
        id_list_size: int = struct_unpack_from(id_list_size_format, buffer=data, offset=base_offset)[0]

        shell_item_data_list: list[bytes] = []

        offset = base_offset + struct_calcsize(id_list_size_format)
        read_data = 0
        while (read_data + len(cls.TERMINAL_ID)) < id_list_size:
            item_id_size: int = struct_unpack_from('<H', buffer=data, offset=offset)[0]

            # Add the item id size and actual data to a list.
            shell_item_data_list.append(bytes(data[offset:offset+item_id_size]))

            offset += item_id_size
            read_data += item_id_size

        if (observed_terminal_id := data[offset:offset+len(cls.TERMINAL_ID)]) != cls.TERMINAL_ID:
            raise MissingTerminalIDError(
                observed_terminal_id=bytes(observed_terminal_id),
                expected_terminal_id=cls.TERMINAL_ID
            )

        # TODO: Support more `ShellItem` types?
        shell_items: list[ShellItem | bytes] = []
        for shell_item_data in shell_item_data_list:
            try:
                shell_items.append(
                    ShellItem.from_bytes(
                        data=shell_item_data,
                        base_offset=0,
                        system_default_encoding=system_default_encoding
                    )
                )
            except KeyError:
                shell_items.append(shell_item_data)

        return cls(shell_items)

    @property
    def path(self) -> PureWindowsPath | None:
        path_segments: list[str] = []
        for link_target in self.__iter__():
            if isinstance(link_target, VolumeShellItem):
                if link_target.name:
                    path_segments.append(link_target.name)
            elif isinstance(link_target, FileEntryShellItem):
                path_segments.append(link_target.primary_name)

        if not path_segments:
            return None

        return PureWindowsPath(*path_segments)
