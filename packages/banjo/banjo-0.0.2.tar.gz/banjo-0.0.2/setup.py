from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='banjo',
    version='0.0.2',
    description='Not a placeholder for an internal library',
    url='',
    author='Max He',
    author_email='pypi@mail.maxhe.org',
    packages=['banjo'],
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ],
)
