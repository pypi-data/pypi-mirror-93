import os.path
import sys
import warnings

from setuptools import find_packages, setup

if sys.version_info < (2, 7):
    raise NotImplementedError(
        """\n
##############################################################
# globus-sdk does not support python versions older than 2.7 #
##############################################################"""
    )

# warn on older/untested python3s
# it's not disallowed, but it could be an issue for some people
if sys.version_info > (3,) and sys.version_info < (3, 6):
    warnings.warn(
        "Installing globus-sdk on Python 3 versions older than 3.6 "
        "may result in degraded functionality or even errors."
    )


# single source of truth for package version
version_ns = {}
with open(os.path.join("globus_sdk", "version.py")) as f:
    exec(f.read(), version_ns)

setup(
    name="globus-sdk",
    version=version_ns["__version__"],
    description="Globus SDK for Python",
    long_description=open("README.rst").read(),
    author="Globus Team",
    author_email="support@globus.org",
    url="https://github.com/globus/globus-sdk-python",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "requests>=2.9.2,<3.0.0",
        "six>=1.10.0,<2.0.0",
        "pyjwt[crypto]>=1.5.3,<2.0.0",
    ],
    extras_require={
        # empty extra included to support older installs
        "jwt": [],
        # the development extra is for SDK developers only
        "development": [
            # drive testing with tox
            "tox>=3.5.3,<4.0",
            # linting
            "flake8>=3.0,<4.0",
            'isort>=5.6.4,<6.0;python_version>="3.6"',
            'black==20.8b1;python_version>="3.6"',
            # flake-bugbear requires py3.6+
            'flake8-bugbear==20.11.1;python_version>="3.6"',
            # testing
            "pytest<5.0",
            "pytest-cov<3.0",
            "pytest-xdist<2.0",
            # mock on py2
            'mock==2.0.0;python_version<"3.6"',
            # mocking HTTP responses
            "responses==0.12.1",
            # pyinstaller is needed in order to test the pyinstaller hook
            'pyinstaller;python_version>="3.6"',
            # builds + uploads to pypi
            'twine>=3,<4;python_version>="3.6"',
            'wheel==0.36.2;python_version>="3.6"',
            # docs
            'sphinx==3.4.3;python_version>="3.6"',
            'sphinx-material==0.0.32;python_version>="3.6"',
        ],
    },
    entry_points={
        "pyinstaller40": ["hook-dirs = globus_sdk._pyinstaller:get_hook_dirs"]
    },
    include_package_data=True,
    keywords=["globus", "file transfer"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
