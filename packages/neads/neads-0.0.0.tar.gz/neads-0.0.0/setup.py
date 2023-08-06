import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.rst').read_text()


def parse_requirements_file(filename):
    with open(filename, encoding="utf-8") as fid:
        requires = [l.strip() for l in fid.readlines() if l]

    return requires


install_requires = parse_requirements_file('requirements.txt')

data = ['requirements.txt', 'LICENSE.txt', 'INSTALL.rst', 'README.rst']


setup(
    name='neads',
    version='0.0.0',
    description='Modular tool to analysis of dynamic system with an '
                'inherent network structure.',
    long_description=README,
    url='https://www.cs.cas.cz/hartman/neads/',
    author='Tomáš Hons, David Hartman, Jaroslav Hlinka',
    author_email='Hons.T.m@seznam.cz',
    license='GPL3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    packages=[
        'neads',
        'neads.error_handlers',
        'neads.examples',
        'neads.tutorials',
        'plugins',
        'plugins.loaders',
        'plugins.preprocessors',
        'plugins.evolvers',
        'plugins.builders',
        'plugins.weighted_editors',
        'plugins.filters',
        'plugins.unweighted_editors',
        'plugins.analyzers',
        'plugins.finalizers'
    ],
    install_requires=install_requires,
    data_files=data
)