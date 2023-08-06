"""Install the pynmdc Package"""
import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8').read()
VERSION = open(os.path.join(BASE_DIR, 'VERSION'), encoding='utf-8').read()

INSTALL_REQUIRES = [
    pkg for pkg in open('requirements.txt').readlines()
]

PYTHON_REQUIRES = '>=3.5.*'


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)


setup(
    name='nmdc',
    version=VERSION,
    description="Command line toolbox of NMDC (https://microbiomedata.org/)",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='NMDC, microbiome, bioinformatics',
    author='Bin Hu',
    author_email='bhu@lanl.gov',
    url='https://microbiomedata.org/',
    license='BSD 3 "Clause"',
    packages=find_packages('src', exclude=["*.test"]),
    package_dir={'': 'src'},
    package_data={},
    include_package_data=False,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
        },
    entry_points={
        'console_scripts': ['nmdc = nmdc.scripts.__main__:nmdccli']
        }
)
