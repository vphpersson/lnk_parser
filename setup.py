from setuptools import setup, find_packages

setup(
    name='lnk_parser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'msdsalgs @ https://github.com/vphpersson/msdsalgs/tarball/master',
    ]
)
