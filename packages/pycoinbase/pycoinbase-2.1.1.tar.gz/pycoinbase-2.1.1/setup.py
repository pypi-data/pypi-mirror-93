# coding: utf-8
import os
from setuptools import setup
import pycoinbase.wallet

README = open(os.path.join(os.path.dirname(__file__), 'PYPIREADME.rst')).read()
REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

setup(
    name='pycoinbase',
    version=pycoinbase.wallet.__version__,
    packages=['pycoinbase', 'pycoinbase.wallet'],
    include_package_data=True,
    license='Apache 2.0',
    description='Updated Coinbase API client library',
    long_description=README,
    url='https://github.com/anton-stefanovich/pycoinbase/',
    keywords=['api', 'pycoinbase', 'bitcoin', 'oauth2', 'client'],
    install_requires=REQUIREMENTS,
    author='Anton Stefanovich',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
