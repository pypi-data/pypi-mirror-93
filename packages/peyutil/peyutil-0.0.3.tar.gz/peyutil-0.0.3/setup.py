#!/usr/bin/env python
import sys
import os

# setup.py largely based on
#   http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
# Also see Jeet Sukumaran's DendroPy

###############################################################################
# setuptools/distutils/etc. import and configuration
try:
    # noinspection PyUnresolvedReferences
    import ez_setup

    try:
        ez_setup_path = " ('" + os.path.abspath(ez_setup.__file__) + "')"
    except OSError:
        ez_setup_path = ""
    sys.stderr.write("using ez_setup%s\n" % ez_setup_path)
    ez_setup.use_setuptools()
    # noinspection PyUnresolvedReferences
    import setuptools

    try:
        setuptools_path = " ('" + os.path.abspath(setuptools.__file__) + "')"
    except OSError:
        setuptools_path = ""
    sys.stderr.write("using setuptools%s\n" % setuptools_path)
    # noinspection PyUnresolvedReferences
    from setuptools import setup, find_packages
except ImportError as e:
    sys.stderr.write("using distutils\n")
    from distutils.core import setup

    sys.stderr.write("using canned package list\n")
    PACKAGES = ['peyutil',
                'peyutil.test',
                'peyutil.test.support',
                ]
    EXTRA_KWARGS = {}
else:
    sys.stderr.write("searching for packages\n")
    PACKAGES = find_packages()
    EXTRA_KWARGS = dict(
        include_package_data=True,
        test_suite="peyutil.test"
    )

EXTRA_KWARGS["zip_safe"] = True
ENTRY_POINTS = {}
EXTRA_KWARGS['scripts'] = []

###############################################################################
# setuptools/distuils command extensions
try:
    from setuptools import Command
except ImportError:
    sys.stderr.write("setuptools.Command could not be imported: setuptools extensions not available\n")
else:
    sys.stderr.write("setuptools command extensions are available\n")
    command_hook = "distutils.commands"
    ENTRY_POINTS[command_hook] = []

setup(
    name='peyutil',
    version='0.0.3',  # sync with __version__ in peyutil/__init__.py
    description='Utility functions used by other python packages written by the  Open Tree of Life team',
    long_description=(open('README.rst').read()),
    url='https://github.com/OpenTreeOfLife/peyutil',
    license='BSD',
    author='Emily Jane B. McTavish and Mark T. Holder',
    author_email='mtholder@gmail.com',
    py_modules=['peyutil'],
    install_requires=['setuptools', 'wheel'],
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords=['bioinformatics', 'utility', 'phylogenetics'],
    **EXTRA_KWARGS
)
