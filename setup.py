from setuptools import setup, find_packages

setup(
    name='lnk_parser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'msdsalgs @ git+ssh://git@github.com/vphpersson/msdsalgs.git#egg=msdsalgs',
        'pyutils @ git+ssh://git@github.com/vphpersson/pyutils.git#egg=pyutils'
    ]
)
