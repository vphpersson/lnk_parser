from __future__ import annotations
from logging import getLogger
from dataclasses import dataclass, field
from typing import Optional
from struct import unpack_from as struct_unpack_from, pack as struct_pack
from re import sub as re_sub

from pyutils.my_string import underline, text_align_delimiter

from lnk_parser.structures.shell_link_header import ShellLinkHeader
from lnk_parser.structures.link_target_id_list import LinkTargetIDList
from lnk_parser.structures.link_info import LinkInfo
from lnk_parser.utils import _read_string_data_field
from lnk_parser.structures.extra_data import ExtraData, UnsupportedExtraData

LOG = getLogger(__name__)


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
    extra_data_list: list[ExtraData] = field(default_factory=list)

    # TODO: Add `strict` parameter.
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

        string_data_kwargs: dict[str, str] = {}
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

        extra_data_list: list[ExtraData] = []

        while True:
            try:
                extra_data = ExtraData.from_bytes(data=data, base_offset=offset)
                block_size = extra_data.BLOCK_SIZE if extra_data is not None else None
            except KeyError:
                extra_data = UnsupportedExtraData.from_bytes(data=data, base_offset=offset)
                LOG.warning(
                    f'No supported `ExtraData` structure for signature `0x{extra_data.signature:02x}`.'
                )
                block_size = extra_data.block_size

            if extra_data is None:
                offset += 4
                break

            offset += block_size
            extra_data_list.append(extra_data)

        return cls(
            header=ShellLinkHeader.from_bytes(data=data),
            link_target_id_list=link_target_id_list,
            link_info=link_info,
            **string_data_kwargs,
            extra_data_list=extra_data_list
        )

    def __str__(self) -> str:
        link_target_str: str = '\n\n'.join(str(link_target_id) for link_target_id in self.link_target_id_list)
        extra_data_str: str = '\n\n'.join(str(extra_data) for extra_data in self.extra_data_list)

        # TODO: Add `LinkInfo` string.

        return text_align_delimiter(
            text=re_sub(
                pattern=r'\s+$',
                repl='',
                string=(
                    f'{underline(string="General", underline_character="-")}\n'
                    f'Link target: {self.link_target_id_list.path}\n'
                    f'Arguments: {self.command_line_arguments}\n'
                    f'Name string: {self.name_string}\n'
                    f'Relative path: {self.relative_path}\n'
                    f'Working dir: {self.working_dir}\n'
                    f'Icon location: {self.icon_location}\n'
                    f'{underline(string="Header", underline_character="-")}\n'
                    f'{self.header}\n'
                    f'{underline(string="Link target IDs", underline_character="-")}\n'
                    f'{link_target_str}\n'
                    f'{underline(string="Extra data", underline_character="-")}\n'
                    f'{extra_data_str}\n'
                )
            ),
            delimiter=': ',
            put_non_match_after_delimiter=False
        )
