import os
import re

import setuptools


def get_version():
    with open(os.path.join("aiotailf", "__init__.py")) as f:
        content = f.read()
        return re.search('__version__ = "(.*?)"', content).group(1)


def strip_comments(comments):
    return comments.split("#", 1)[0].strip()


def reqs(*f):
    return list(
        filter(
            None,
            [
                strip_comments(s)
                for s in open(os.path.join(os.getcwd(), *f)).readlines()
            ],
        )
    )


setuptools.setup(
    name="aiotailf",
    version=get_version(),
    author="nocilantro",
    url="https://github.com/YangzhenZhao/aiotailf",
    install_requires=reqs("requirements.txt"),
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        tailf=aiotailf.cli:cli
    """,
)
