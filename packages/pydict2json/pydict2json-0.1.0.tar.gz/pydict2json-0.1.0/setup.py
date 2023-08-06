#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import pathlib
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

VERSION = '0.1.0'

HERE = pathlib.Path(__file__).parent

long_description = (HERE / "README.md").read_text()

class UploadCommand(Command):
    """
    Support setup.py upload.
    ref.: https://github.com/navdeep-G/setup.py
    """

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


setup(
    name='pydict2json',
    version=VERSION,
    description='Given a printed python dict, convert it to JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Robert Alexander',
    author_email='raalexander.phi@gmail.com',
    url='https://github.com/ralexander-phi/python-str-dict-to-json',

    python_requires='>=3.6',
    install_requires=[
        'click>=7.1.2',
      ],
    extras_require={},

    packages=['pydict2json'],
    entry_points={
        'console_scripts': ['pydict2json=__main__:main'],
    },
    include_package_data=True,

    license='MIT',
    classifiers=[
        # See: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

