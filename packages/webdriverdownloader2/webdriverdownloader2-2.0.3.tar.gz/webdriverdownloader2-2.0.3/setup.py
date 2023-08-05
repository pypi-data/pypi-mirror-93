from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="webdriverdownloader2",
    version="2.0.3",
    description="Python module and CLI tool for facilitating download and deploy of WebDriver binaries.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    url="https://github.com/bodharma/webdriverdownloader2",
    authors="Leonides T. Saguisag Jr.",
    author_email="leonidessaguisagjr@gmail.com",
    maintainer="Bohdan Lesiv",
    maintainer_email="boghdanlesiv@gmail.com",
    license="MIT",
    packages=["webdriverdownloader2"],
    install_requires=["beautifulsoup4", "requests", "tqdm", "loguru", "py-cpuinfo"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "webdriverdownloader2 = webdriverdownloader2.cli:main",
        ],
    },
)
