import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='divvy.fps',
    version = '0.1.5dev',
    author='Divvyshot, Inc.',
    description='Library for working with Amazon Flexible Payment Service',
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license = "proprietary",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['divvy'],
    install_requires=[
        'setuptools',
        ],
    include_package_data = True,
    zip_safe = False,
    )
