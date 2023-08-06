import os

from dotenv import load_dotenv

load_dotenv()

NAME = "settings-master"
VERSION = "0.1.1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_path_to_readme = os.path.join(BASE_DIR, "README.md")

with open(_path_to_readme) as f:
    LONG_DESCRIPTION = f.read()

AUTHOR = "semenInRussia"
AUTHOR_EMAIL = "hrams205@gmail.com"

URL = "https://github.com/semenInRussia/FreeSpotify_back"

LICENSE = "MIT"
