import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read():
    return open("../README.md").read()

setup(
    name = "gpc",
    version = "0.0.1",
    author = "Koren Minchev",
    author_email = "korenminchev@gmail.com",
    description = ("Generic Packet Communicator"),
    license = "BSD",
    url = "https://github.com/Koren13n/GPC",
    long_description=read(),
    entry_points = {
        'console_scripts': ['gpc=gpc.__main__:main'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)