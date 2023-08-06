import codecs
import os
import sys
from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


long_description = read('README.md')

setup(
    name="hdob",
    version=get_version("src/hdob/__init__.py"),
    author="House.Chou",
    author_email="hoare.tw@gmail.com",
    description="Hex, Decimal, Octal, Binary converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="GUI UI tkinter Converter",
    url="https://github.com/housechou/hdob",
    python_requires=">=3.5",
    package_dir={'': 'src'},
    packages=find_packages(
        where="src",
    ),
    entry_points={
	"console_scripts": [
            "hdob=hdob.hdob:main"
	],
	"gui_scripts": [
            "hdob=hdob.hdob:main"
	],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Operating System :: OS Independent"
    ),
)
