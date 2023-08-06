import os

from dotenv import load_dotenv

load_dotenv()

NAME = "settings-master"
VERSION = "0.1.2"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)


_path_to_readme = os.path.join(ROOT_DIR, "README.md")

with open(_path_to_readme) as f:
    LONG_DESCRIPTION = f.read()

AUTHOR = "semenInRussia"
AUTHOR_EMAIL = "hrams205@gmail.com"

LICENSE = "MIT"
