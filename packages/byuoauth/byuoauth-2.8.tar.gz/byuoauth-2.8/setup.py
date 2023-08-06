import setuptools
import json

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('version.json', 'r') as f:
    version_number = json.load(f)['version']

setuptools.setup(
    name="byuoauth",
    version=version_number,
    author="Mark Roth",
    author_email="mark_roth@byu.edu",
    description="Scripts to easily allow BYU applications to generate OAuth tokens and JWTs for test use.",
    long_description=long_description,
    url="https://github.com/byu-oit/python-token-scripts",
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License ',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.0',
    install_requires=[
        'requests >= 2.7.0, < 3.0.0'
    ]
)
