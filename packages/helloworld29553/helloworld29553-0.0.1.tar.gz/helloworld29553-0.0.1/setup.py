from setuptools import setup
# Don't use distutils

# Configuration
setup(
    # Name on pip, what you pip-install
    name='helloworld29553',

    url="https://github.com/elunna/helloworld",
    author="Erik Lunna",
    author_email="eslunna@gmail.com",
    # 0.0.x - says that it is unstable.
    version='0.0.1',

    description='Say hello',

    # list of the python code modules to install
    py_modules=["helloworld"],

    # Where the code is
    package_dir={'': 'src'},
)

# See https://pypi.org/classifiers
classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "Operating System :: OS Independent",
],

