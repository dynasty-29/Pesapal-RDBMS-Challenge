from setuptools import setup, find_packages

setup(
    name="pesapal-rdbms",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pyparsing',
        'tabulate',
    ],
)