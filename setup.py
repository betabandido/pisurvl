from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pisurvl',
    # Versions should comply with PEP440.
    version='0.0.5',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pisurvl-server = pisurvl.main:main'
        ]
    },
    install_requires=[
        'google-api-python-client',
        'imutils',
        'mockito',
        'numpy',
        'oauth2client',
        'parameterized',
        'Pillow',
        'pytest',
        'PyYAML'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # Metadata for upload to PyPI
    author='Victor Jimenez',
    author_email='betabandido@gmail.com',
    description='A surveillance system based on Raspberry Pi',
    long_description=long_description,
    license='GPLv3',
    keywords='surveillance camera home-automation',
    url='https://github.com/betabandido/pisurv',
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
        'Programming Language :: Python :: 3.6',
    ],
)
