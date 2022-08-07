from setuptools import setup, find_packages

setup(
    name='lnk_parser',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'strings_utils_py @ git+https://github.com/vphpersson/string_utils_py.git#egg=string_utils_py',
        'parsing_error @ git+https://github.com/vphpersson/parsing_error.git#egg=parsing_error',
        'typed_argument_parser @ git+https://github.com/vphpersson/typed_argument_parser.git#egg=typed_argument_parser',
        'msdsalgs @ git+https://github.com/vphpersson/msdsalgs.git#egg=msdsalgs'
    ]
)
