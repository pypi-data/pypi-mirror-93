"""The setup script."""

import glob
import collections
from pathlib import Path
import os
from os import environ

from setuptools import find_packages, setup

PROJECT = Path(__file__).parent
PACKAGE_NAME = "pulmoscan"

def create_data_files_structure():
    data_files = collections.defaultdict(list)

    for filename in glob.iglob('resources/**/*', recursive=True):
        if os.path.isdir(str(filename)):
            continue
        directory = os.path.dirname(filename)
        directory = os.path.join('pulmoscan_resources', directory)
        data_files[directory].append(filename)

    return list(data_files.items())


setup(
    name=PACKAGE_NAME,
    version="0.1.4" + environ.get('VERSION_SUFFIX', ''),
    license="Proprietary",
    description="An example Python project",
    long_description=PROJECT.joinpath("README.md").read_text(encoding="utf-8"),
    keywords=["python"],
    author="Andrew Naumovich",
    author_email="andrew.naumovich@yandex.ru",
    url="https://github.com/NandreyN/PulmoAI",
    packages=find_packages(),
    package_dir={"": "."},
    python_requires=">=3.6",
    data_files=create_data_files_structure(),
    package_data={"pulmoscan": [
        "../scripts/copy_resources.py",
        "../resources/test/*.*",
        "../resources/mappings/*.*",
        "../train.py"
    ]},
    install_requires=PROJECT.joinpath("requirements-dev.in").read_text().split("\n"),
    # see https://github.com/python/mypy/issues/8802 & PEP 561
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pulmoscan_train=train:entry',
            'pulmoscan_copy_resources=scripts.copy_resources:entry'
        ],
    },
)
