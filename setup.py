from setuptools import setup, find_packages

setup(
    name='lnk_parser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'msdsalgs @ git+https://github.com/vphpersson/msdsalgs.git#egg=msdsalgs',
        'pyutils @ git+https://github.com/vphpersson/pyutils.git#egg=pyutils'
    ]
)
