#!/usr/bin/env python3

from __future__ import annotations
from argparse import ArgumentParser, FileType, Namespace as ArgparseNamespace

from lnk_parser.structures.shell_link import ShellLink

# TODO: Add tests? (pytest)


class LnkArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument('lnk_files', nargs='+', type=FileType('rb'), metavar='lnk_file')


def main():
    args: ArgparseNamespace = LnkArgumentParser().parse_args()

    print(
        '\n\n'.join(
            str(ShellLink.from_bytes(data=lnk_file.read())) for lnk_file in args.lnk_files
        )
    )


if __name__ == '__main__':
    main()
