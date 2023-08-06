#!/usr/bin/env python
"""apu: Antons Python Utilities."""

# Third party
from setuptools import setup

requires_designpattern = ["dill"]
requires_datetime = ["pytz", "pint", "tzlocal"]
requires_setup = ["GitPython"]
requires_geographie = ["numpy"]
requires_io = [
    "numpy", "h5py", "mat4py", "pyyaml", "python_magic", "dill", "msgpack"
]
requires_ml = ["torch"]
requires_all = (requires_datetime + requires_setup + requires_geographie +
                requires_designpattern + requires_io + requires_ml)

setup(
    version="0.1.7",
    package_data={"apu": []},
    project_urls={
        'Documentation': 'https://afeldman.github.io/apu/',
        'Source': 'https://github.com/afeldman/apu',
        'Tracker': 'https://github.com/afeldman/apu/issues',
    },
    extras_require={
        "all": requires_all,
        "datetime": requires_datetime,
        "setup": requires_setup,
        "geo": requires_geographie,
        "designpattern": requires_designpattern
    },
)