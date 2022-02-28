from io import BufferedReader
from argparse import FileType

from typed_argument_parser import TypedArgumentParser


class LnkParserArgumentParser(TypedArgumentParser):

    class Namespace:
        lnk_files: list[BufferedReader]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument('lnk_files', nargs='+', type=FileType('rb'), metavar='lnk_file')
