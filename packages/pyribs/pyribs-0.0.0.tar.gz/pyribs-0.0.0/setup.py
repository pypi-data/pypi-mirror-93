"""Warning package for pyribs.

Based on the one for PyTorch: https://pypi.org/project/pytorch/
"""
import sys
from distutils.core import setup

MESSAGE = 'You tried to install "pyribs". The package named for pyribs is "ribs"'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install
    (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(MESSAGE)

if argv('bdist_wheel'):  # modern pip install
    raise Exception(MESSAGE)

setup(
    name='pyribs',
    version='0.0.0',
    maintainer="Bryon Tjanaka",
    maintainer_email="bryon@btjanaka.net",
    url="https://github.com/icaros-usc/pyribs",
    long_description=MESSAGE,
)
