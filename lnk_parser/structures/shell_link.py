from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
from struct import unpack_from as struct_unpack_from
from re import sub as re_sub

from lnk_parser.structures.shell_link_header import ShellLinkHeader
from lnk_parser.structures.link_target_id_list import LinkTargetIDList
from lnk_parser.structures.link_info import LinkInfo
from lnk_parser.utils import _read_string_data_field


@dataclass
class ShellLink:
    header: ShellLinkHeader
    link_target_id_list: Optional[LinkTargetIDList] = None
    link_info: Optional[LinkInfo] = None
    name_string: Optional[str] = None
    relative_path: Optional[str] = None
    working_dir: Optional[str] = None
    command_line_arguments: Optional[str] = None
    icon_location: Optional[str] = None
    extra_data: Optional[bytes] = None

    @classmethod
    def from_bytes(cls, data: bytes, base_offset: int = 0) -> ShellLink:
        """
        Make a shell link from a sequence of bytes.

        :param data: A byte sequence from which to extract the bytes constituting the shell link.
        :param base_offset: The offset from the start of the byte sequence from where to start extracting.
        :return: A shell link.
        """

        header = ShellLinkHeader.from_bytes(data=data)
        offset = base_offset + header.SIZE

        if header.link_flags.has_link_target_id_list:
            link_target_id_list = LinkTargetIDList.from_bytes(data=data, base_offset=offset)
            offset += struct_unpack_from('<H', buffer=data, offset=offset)[0] + len(LinkTargetIDList.TERMINAL_ID)
        else:
            link_target_id_list = None

        if header.link_flags.has_link_info:
            link_info = LinkInfo.from_bytes(data=data, base_offset=offset)
            offset += link_info.size
        else:
            link_info = None

        string_data_kwargs: Dict[str, str] = {}
        pairs = [
            (header.link_flags.has_name, 'name_string'),
            (header.link_flags.has_relative_path, 'relative_path'),
            (header.link_flags.has_working_dir, 'working_dir'),
            (header.link_flags.has_arguments, 'command_line_arguments'),
            (header.link_flags.has_icon_location, 'icon_location')
        ]

        for string_data_present, field_name in pairs:
            if not string_data_present:
                continue

            string_value, size = _read_string_data_field(
                buffer=data,
                is_unicode=header.link_flags.is_unicode,
                offset=offset,
            )
            offset += size

            string_data_kwargs[field_name] = string_value

        return cls(
            header=ShellLinkHeader.from_bytes(data=data),
            link_target_id_list=link_target_id_list,
            link_info=link_info,
            **string_data_kwargs
        )

    def __str__(self) -> str:
        return re_sub(
            pattern=r'\s+$',
            repl='',
            string=(
                f'Link target: {self.link_target_id_list.path}\n'
                + (f'Arguments: {self.command_line_arguments}\n' if self.command_line_arguments else '')
                + f'Show command: {self.header.show_command.name}\n'
                + (f'Name string: {self.name_string}\n' if self.name_string else '')
                + (f'Relative path: {self.relative_path}\n' if self.relative_path else '')
                + (f'Working dir: {self.working_dir}\n' if self.working_dir else '')
                + (f'Icon location: {self.icon_location}\n' if self.icon_location else '')
            )
        )
