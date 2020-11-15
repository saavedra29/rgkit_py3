#!/usr/bin/env python
'''
Run: ./setup.py register sdist upload
Check: ./setup.py checkdocs (pip install collective.checkdocs)
'''

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    long_description = readme_file.read()

setup(
    name='rgkit_py3',
    version='1.1.1',
    description='Game Engine for Robot Game',
    maintainer='Aristeidis Tomaras',
    maintainer_email='arisgold29@gmail.com',
    url='https://github.com/saavedra29/rgkit_py3',
    packages=find_packages(),
    package_data={'rgkit': ['bots/*.py', 'maps/*.py']},
    license='Unlicense',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'rgrun = rgkit.run:main',
            'rgmap = rgkit.mapeditor:main'
        ]
    },
)
