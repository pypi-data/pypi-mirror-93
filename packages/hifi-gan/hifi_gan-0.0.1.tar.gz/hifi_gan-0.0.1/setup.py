import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hifi_gan",
    version = "0.0.1",
    author = "Zach Wener-Fligner",
    author_email = "zbwener@gmail.com",
    description = "Package up hifi-gan",
    license = "MIT",
    keywords = "speech synthesis machine learning",
    url = "https://github.com/zachwe/hifi_gan",
    packages=['hifi_gan'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
