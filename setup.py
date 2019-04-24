import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='auprico-core',
    version='0.1',
    packages=['auprico_core'],
    description='automated processes and intelligent components - core package',
    long_description=README,
    author='Daniele Bernardini',
    author_email='daniele.bernardini@aismart.co',
    url='https://github.com/dani0805/auprico-core/',
    license='Apache',
    install_requires=[
        'Django>=2.1',
    ]
)