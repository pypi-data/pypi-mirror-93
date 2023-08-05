# -*- coding: utf-8 -*-

"""
"""

import setuptools

import vdown

with open("README.md") as fp:
    README = fp.read()


with open("requirements.txt") as fp:
    text = fp.read()
    REQUIREMENTS = text.split("\n")


setuptools.setup(
    author="drunkdream",
    author_email="drunkdream@qq.com",
    name="vdown",
    license="MIT",
    description="A tool for download m3u8/youtube videos.",
    version=vdown.VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/drunkdream/video-downloader",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=REQUIREMENTS,
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
    ],
    entry_points={
        "console_scripts": [
            "vdown = vdown.cmd:main",
        ],
    },
)
