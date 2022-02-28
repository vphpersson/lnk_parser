#!/usr/bin/env python3

from __future__ import annotations
from typing import Type
from logging import WARNING, StreamHandler, Formatter
from sys import stderr

from string_utils_py import text_align_delimiter, underline

from lnk_parser.cli import LnkParserArgumentParser
from lnk_parser.structures.shell_link import ShellLink, LOG

# TODO: Add tests? (pytest)


def main():
    args: Type[LnkParserArgumentParser.Namespace] = LnkParserArgumentParser().parse_args()

    LOG.setLevel(level=WARNING)
    handler = StreamHandler(stream=stderr)
    handler.setFormatter(fmt=Formatter(fmt='%(levelname)s: %(message)s'))
    LOG.addHandler(hdlr=handler)

    print(
        text_align_delimiter(
            text='\n\n'.join(
                (
                    f'{underline(string=lnk_file.name, underline_character="=")}\n'
                    f'{ShellLink.from_bytes(data=lnk_file.read())}'
                )
                for lnk_file in args.lnk_files
            ),
            delimiter=': ',
            put_non_match_after_delimiter=False
        )
    )


if __name__ == '__main__':
    main()
