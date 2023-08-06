# -*- coding:utf-8 -*-
import os
import codecs

try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "This module could not be installed, probably because"
        " setuptools is not installed on this computer."
        "\nInstall ez_setup ([sudo] pip install ez_setup) and try again."
    )


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pre_version = get_version("GLXCurses/__init__.py")
if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    if os.environ.get("CI_JOB_ID"):
        version = os.environ["CI_JOB_ID"]
    else:
        version = pre_version

with open("README.md") as f:
    long_description = f.read()

setup(
    name="galaxie-curses",
    version=version,
    description="Galaxie Curses is a free software ToolKit for the NCurses API",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    url="https://gitlab.com/Tuuux/galaxie-curses",
    author=["Tuuux", "Mo"],
    author_email="tuxa@rtnp.org",
    license="GNU GENERAL PUBLIC LICENSE Version 3",
    packages=["GLXCurses", "GLXCurses.libs", "GLXCurses.libs.handlers"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["green", "wheel"],
    tests_require=["pyperclip", "wheel", "Pillow"],
    install_requires=["pyperclip", "wheel", "Pillow"],
)
