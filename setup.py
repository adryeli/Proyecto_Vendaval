from setuptools import setup, find_packages

setup(
    name="vendaval",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
        'pytest-mock'
    ],
)
