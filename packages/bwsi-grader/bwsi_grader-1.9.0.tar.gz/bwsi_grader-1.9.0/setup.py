import versioneer
from setuptools import find_packages, setup

DISTNAME = "bwsi_grader"
LICENSE = "MIT"
AUTHOR = "Ryan Soklaski"
AUTHOR_EMAIL = "ry26099@mit.edu"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Education",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
]

INSTALL_REQUIRES = ["numpy >= 1.10"]
TESTS_REQUIRE = ["pytest >= 3.8", "hypothesis >= 4.0"]

DESCRIPTION = "A suite of auto-graders for the BWSI EdX courses."
LONG_DESCRIPTION = """
A package to be utilized locally by students to grade assignments that 
are written in Python. These graders correspond to coursework associated 
with BWSI-EdX.
"""


setup(
    name=DISTNAME,
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    python_requires=">=3.6",
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
            "solutions",
            "solutions.*",
            "bwsi_solutions",
            "bwsi_solutions*",
        ]
    ),
)
