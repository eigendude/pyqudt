################################################################################
#
#  Copyright (C) 2019 Garrett Brown
#  This file is part of pyqudt - https://github.com/eigendude/pyqudt
#
#  pyqudt is derived from jQUDT
#  Copyright (C) 2012-2013  Egon Willighagen <egonw@users.sf.net>
#
#  SPDX-License-Identifier: BSD-3-Clause
#  See the file LICENSE for more information.
#
################################################################################

import setuptools


with open('README.md') as file:
    long_description = file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='pyqudt',
    version='2.0.0',
    author='Garrett Brown',
    author_email='themagnificentmrb@gmail.com',
    description='Python library for working with the QUDT (Quantity, Unit, Dimension and Type) ontology.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eigendude/pyqudt',
    license='BSD-3-Clause',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    packages=setuptools.find_packages(exclude=['test', 'test.*']),
    package_data={
        'qudt.ontology.resources': ['*'],
        'qudt.ontology.resources.v2_1_4': ['*'],
        'qudt': ['py.typed'],
    },
    install_requires=requirements,
)
