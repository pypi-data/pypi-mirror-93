# Copyright (c) 2020-2021, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of Micro-CI, which is released under the BSD 3-Clause License.

"""Setup and metadata for the Micro-CI package."""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

# For details on the metadata specification, have a look at the example or the documentation:
# https://github.com/pypa/sampleproject/blob/master/setup.py
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

setup(
    name="micro_ci",
    description="Micro-CI: A minimalist runner for GitLab CI configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gauss-ml-open/micro-ci",
    author="Edgar Klenske",
    author_email="edgar.klenske@gauss-ml.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="development",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    install_requires=["pyyaml"],
    extras_require={
        "dev": ["black", "flake8", "mypy", "pylint", "rope"],
        "test": ["flaky", "pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "mci=micro_ci:main",
        ]
    },
)
