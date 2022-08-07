from io import BufferedReader
from argparse import FileType

from typed_argument_parser import TypedArgumentParser


class LnkParserArgumentParser(TypedArgumentParser):

    class Namespace:
        lnk_files: list[BufferedReader]
        system_encoding: str | None

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(description='A parser for Shell Link (.LNK) files.') | kwargs
            )
        )

        self.add_argument(
            'lnk_files',
            help='The path of an LNK file to be parsed.',
            nargs='+',
            type=FileType('rb'),
            metavar='lnk_file'
        )

        self.add_argument(
            '--system-encoding',
            help=(
                'The default encoding on the system from which the LNK file originated. Defaults to that of the current'
                ' system.'
            )
        )
