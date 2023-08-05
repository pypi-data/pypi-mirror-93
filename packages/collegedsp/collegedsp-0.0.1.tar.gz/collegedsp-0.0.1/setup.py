from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name = "collegedsp",
    version = "0.0.1",
    description = "Digital Signal Processing Module",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["main"],
    package_dir = {'':'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "numpy~=1.18.0",
        "matplotlib~=3.1.2"
    ],
    extras_require = {
        "dev":[
            "pytest >= 3.7",
        ],
    },
    url = "https://github.com/Ayush-Khamrui/dsprocessing.git",
    author = "Ayush Khamrui",
    author_email = "ayushkhamrui@outlook.com",
)