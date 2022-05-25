import os
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read():
    return open("../README.md").read()

setuptools.setup(
    name = "gepaco",
    version = "0.0.1",
    author = "Koren Minchev",
    author_email = "korenminchev@gmail.com",
    description = ("Generic Packet Communicator"),
    license = "BSD",
    url = "https://github.com/Koren13n/gepaco",
    packages=setuptools.find_packages(),
    install_requires=["uvicorn", "fastapi"],
    long_description=read(),
    package_dir={'gepaco':'gepaco'},
    include_package_data=True,
    entry_points = {
        'console_scripts': ['gepaco=gepaco.__main__:main'],
    },
)