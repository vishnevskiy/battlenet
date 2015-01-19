from setuptools import setup, find_packages
from sys import version_info
from battlenet.version import VERSION

DESCRIPTION = "Python Library for Blizzard's Community Platform API"

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Games/Entertainment',
]

setup(
    name='battlenet',
    version=VERSION,
    packages=find_packages(),
    author='Stanislav Vishnevskiy <vishnevskiy@gmail.com>, Jason Antman <jason@jasonantman.com>',
    author_email='vishnevskiy@gmail.com, jason@jasonantman.com',
    url='https://github.com/vishnevskiy/battlenet',
    license='MIT',
    include_package_data=True,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
)
