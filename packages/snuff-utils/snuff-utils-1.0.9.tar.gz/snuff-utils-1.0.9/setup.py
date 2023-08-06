import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="snuff-utils",
    version="1.0.9",
    description="Universal functions and decorators and some packages extras",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/egorgvo/utils",
    author="Egor Gvo",
    author_email="work.egvo@ya.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["snuff_utils"],
    include_package_data=True,
)
