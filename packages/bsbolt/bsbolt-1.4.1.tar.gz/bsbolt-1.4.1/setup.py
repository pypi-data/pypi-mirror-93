#! /usr/bin/env python3

import os
import subprocess
import sys

if sys.version_info < (3, 6):
    print('Python must be >= 3.6.0')
    raise OSError

try:
    from setuptools import setup
except ImportError as e:
    print('Please install python setuptools, '
          'https://packaging.python.org/tutorials/installing-packages/#use-pip-for-installing ')
    raise e

from setuptools.command.develop import develop
from setuptools.command.build_py import build_py

with open("README.md", "r") as fh:
    long_description = fh.read()

"""
External dependencies compiled for linux using quay.io/pypa/manylinux2010_x86_64 image:
/opt/python/cpXX-cpXX/bin/python setup.py bdist_wheel
"""


class BuildError(Exception):
    """Build error"""
    pass


def compile_dependency(compilation_command, cwd):
    comp = subprocess.Popen(compilation_command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True, cwd=cwd)
    comp.wait()
    if comp.returncode:
        print('Please compile with GCC >= 8.3.1 / zlib-devel >= 1.2.3')
        for line in iter(comp.stderr.readline, ''):
            print(line)
        raise BuildError
    for line in iter(comp.stdout.readline, ''):
        formatted_line = line.strip()
        print(formatted_line)
    for line in iter(comp.stderr.readline, ''):
        formatted_line = line.strip()
        print(formatted_line)


def make_external_dependencies():
    working_directory = os.path.dirname(os.path.realpath(__file__))
    bwa_directory = f'bsbolt/External/BWA'
    htslib_directory = f'bsbolt/External/HTSLIB'
    wgsim_directory = f'bsbolt/External/WGSIM'
    if not os.path.exists(f'{wgsim_directory}/wgsim'):
        print('Compiling wgsim')
        compile_dependency(['make'], wgsim_directory)
    if not os.path.exists(f'{htslib_directory}/stream_bam'):
        print('Compiling htslib')
        compile_dependency(['autoheader'], htslib_directory)
        compile_dependency(['autoconf'], htslib_directory)
        compile_dependency(['./configure', '--disable-bz2', '--disable-lzma'], htslib_directory)
        compile_dependency(['make'], htslib_directory)
    if not os.path.exists(f'{bwa_directory}/bwa'):
        print('Compiling bwa')
        compile_dependency(['make'], bwa_directory)


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None


class DevelopCmd(develop):

    def run(self):
        make_external_dependencies()
        super().run()


class BuildCmd(build_py):

    def run(self):
        make_external_dependencies()
        self.data_files = [('bsbolt', 'bsbolt', 'build/lib/bsbolt', []),
                           ('bsbolt.Align', 'bsbolt/Align', 'build/lib/bsbolt/Align', []),
                           ('bsbolt.CallMethylation', 'bsbolt/CallMethylation', 'build/lib/bsbolt/CallMethylation', []),
                           ('bsbolt.External', 'bsbolt/External', 'build/lib/bsbolt/External',
                            ['WGSIM/wgsim', 'BWA/bwa', 'HTSLIB/stream_bam']),
                           ('bsbolt.Impute', 'bsbolt/Impute', 'build/lib/bsbolt/Impute', []),
                           ('bsbolt.Impute.Imputation', 'bsbolt/Impute/Imputation',
                            'build/lib/bsbolt/Impute/Imputation', []),
                           ('bsbolt.Impute.Impute_Utils', 'bsbolt/Impute/Impute_Utils',
                            'build/lib/bsbolt/Impute/Impute_Utils', []), (
                           'bsbolt.Impute.Validation', 'bsbolt/Impute/Validation', 'build/lib/bsbolt/Impute/Validation',
                           []),
                           ('bsbolt.Index', 'bsbolt/Index', 'build/lib/bsbolt/Index', []),
                           ('bsbolt.Matrix', 'bsbolt/Matrix', 'build/lib/bsbolt/Matrix', []),
                           ('bsbolt.Simulate', 'bsbolt/Simulate', 'build/lib/bsbolt/Simulate', []),
                           ('bsbolt.Utils', 'bsbolt/Utils', 'build/lib/bsbolt/Utils', []),
                           ('bsbolt.Variant', 'bsbolt/Variant', 'build/lib/bsbolt/Variant', [])]
        super().run()


setup(name='bsbolt',
      version='1.4.1',
      description='Bisulfite Sequencing Processing Platform',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/NuttyLogic/BSBolt',
      project_urls={'Documentation': 'https://bsbolt.readthedocs.io/en/latest/'},
      author='Colin P. Farrell',
      author_email='colinpfarrell@gmail.com',
      license='MIT',
      packages=['bsbolt',
                'bsbolt.Align',
                'bsbolt.CallMethylation',
                'bsbolt.Impute',
                'bsbolt.Impute.Imputation',
                'bsbolt.Impute.Impute_Utils',
                'bsbolt.Impute.Validation',
                'bsbolt.Index',
                'bsbolt.Matrix',
                'bsbolt.Simulate',
                'bsbolt.Utils',
                'bsbolt.Variant'],
      classifiers=['Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8'],
      platforms=["Linux", "Mac OS-X", "Unix"],
      requires=['pysam', 'numpy', 'tqdm'],
      install_requires=['pysam>=0.9.1', 'numpy>=1.16.3', 'tqdm>=4.31.1', 'setuptools>=46.0.0'],
      entry_points={'console_scripts': ['bsbolt = bsbolt.__main__:launch_bsb',
                                        'BSBolt = bsbolt.__main__:launch_bsb']},
      python_requires='>=3.6',
      test_suite='tests',
      include_package_data=True,
      cmdclass={'develop': DevelopCmd,
                'build_py': BuildCmd,
                'bdist_wheel': bdist_wheel},
      zip_safe=False
      )
