import setuptools
import json

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('version.json', 'r') as f:
    version_number = json.load(f)['version']

setuptools.setup(
    name='zephyr-sdk',
    version=version_number,
    author='Mark Roth',
    author_email='mark_roth@byu.edu',
    description='A package for helping use the zephyr API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/byu-oit/zephyr-sdk',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License ',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests >= 2.23.0, < 3.0.0'
    ]
)