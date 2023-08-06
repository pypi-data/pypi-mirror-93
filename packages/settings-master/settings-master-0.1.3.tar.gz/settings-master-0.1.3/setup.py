#!/usr/bin/env python
import os
import sys
from distutils.core import setup

from setuptools import find_packages

from settings_master.settings import settings

_is_not_istall = not "install" in sys.argv

path_to_requirements = os.path.join(settings.ROOT_DIR, "requirements.txt")

if _is_not_istall:
    with open(path_to_requirements) as requirements_file:
        text = requirements_file.read()

        install_requires = text.split("\n")
else:
    install_requires = []

packages = find_packages()

setup(
    name=settings.NAME,
    version=settings.VERSION,

    long_description=settings.LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    author=settings.AUTHOR,
    author_email=settings.AUTHOR_EMAIL,

    install_requires=install_requires,
    packages=packages,

    keywords=["settings_master", "settings-master"],

    license=settings.LICENSE,
)
