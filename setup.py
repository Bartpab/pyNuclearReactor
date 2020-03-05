from setuptools import setup, find_packages

import sys
sys.path.append(".")

from nuclear import __version__

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nuclear',
    version=__version__,

    packages=find_packages(),
    
    author="Gael Pabois",
    description="Reactive UI Framework on top of wxPython highly inspired by Vue",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=requirements,
    url='http://github.com/sametmax/sm_lib',
    
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU GPLv3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],

    entry_points = {
        'console_scripts': [],
    },
)