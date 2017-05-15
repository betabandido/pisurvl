from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pisurvl',

    # Versions should comply with PEP440.
    version='0.0.1',

    description='A surveillance system based on Raspberry Pi',
    long_description=long_description,

    url='https://github.com/betabandido/pisurv',

    author='Victor Jimenez',
    author_email='betabandido@gmail.com',

    license='GPLv3',

    package_dir={'': 'src'},

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Home Automation',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='surveillance camera home-automation',

    install_requires=[
        'google-api-python-client',
        'imutils',
        'mockito',
        'numpy',
        'oauth2client',
        'Pillow',
        'pytest',
        'PyYAML'
    ]
)
