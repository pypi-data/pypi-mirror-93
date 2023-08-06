# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Package Details."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="reconcile",  # Replace with your own username
    version="0.0.5",
    author="Charles Unruh",
    author_email="charles.unruh.dev@gmail.com",
    description="A reconciliation loop system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cunruh3760/reconcile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6.8",
    install_requires=install_requires,
)