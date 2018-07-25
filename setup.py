import io
from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = f.read()

INSTALL_DEPS = ['click==6.7',
                'simplesam==0.1.2',
                'six==1.11.0',
                'future>=0.16.0']
DEV_DEPS = ['tox']
TEST_DEPS = ['pytest',
             'pytest-cov'] + DEV_DEPS
LINT_DEPS = ['pylint'] + DEV_DEPS
DOCS_DEPS = ['sphinx >= 1.7.5', 'sphinxcontrib-fulltoc'] + DEV_DEPS

setup(
    name='sam-alignment-reconstructor',

    # https://pypi.python.org/pypi/setuptools_scm
    use_scm_version=True,

    description='SAM Alignment Reconstructor',
    long_description=LONG_DESC,

    url='https://github.com/lairdm/sam-alignment-reconstructor.git',

    author='Matthew Laird',
    author_email='lairdm@ebi.ac.uk',

    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='sam alignment bioinformatics',

    packages=find_packages(exclude=['docs', 'tests']),

    entry_points = {
        'console_scripts': ['sam_alignment_reconstructor=sam_alignment_reconstructor.cli:main'],
        },
      
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=INSTALL_DEPS,

    setup_requires=['setuptools_scm'],

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': DEV_DEPS,
        'test': TEST_DEPS,
        'docs': DOCS_DEPS,
        'lint': LINT_DEPS
    },
)