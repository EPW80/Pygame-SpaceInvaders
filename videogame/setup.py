# Erik Williams
# CPSC 386-02
# 2023-04-20
# epwilliams@csu.fullerton.edu
# @EPW80
#
# Lab 05-00
#
# This is my Space Invaders project!
#

"""
This is my Space Invaders setup
"""
from setuptools import setup

NAME = "Space Invaders videogame"
VERSION = "0.1"
DESCRIPTION = "A package to support writing games with PyGame"

with open("README.md", "r", encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
AUTHOR = "Erik P. Williams"
AUTHOR_EMAIL = "epwilliams@gmail.com"
URL = "https://github.com/EPW80/SpaceInvadersVideogame"
ALT_URL = "https://github.com/cpsc-spring-2023/cpsc-386-05-invaders-EPW80"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
)
