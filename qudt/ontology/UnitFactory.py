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

from qudt.ontology.OntologyReader import OntologyReader
from qudt.ontology.QUDT import QUDT
from qudt.ontology.RDF import RDF
from qudt.ontology.RDFS import RDFS
from qudt import Unit

import os
import rdflib


# The package containing the RDF triplet repositories
REPO_PACKAGE_NAME = 'resources'

# The RDF triplet repositories to load
REPO_FILES = [
    'unit',
    'qudt',
    'quantity',
    'ops.ttl',
]


class UnitFactory(object):
    """
    A factory for creating units of measurement.
    """

    _instance = None

    def __init__(self):
        """
        Create an instance of the unit factory and load the RDF triplet
        repositories.
        """
        # Get the path to this package
        package_path = os.path.dirname(os.path.realpath(__file__))

        # Get the path to the repository files
        self._repo_path = os.path.join(package_path, REPO_PACKAGE_NAME)

        # Load the repositories
        self._repos = [
            self._read_repo(repo_file) for repo_file in REPO_FILES
        ]

    @classmethod
    def _get_instance(cls):
        """
        Get the singleton used to store repository contents.

        :return: The singleton instance of type UnitFactory
        """
        if not cls._instance:
            cls._instance = UnitFactory()

        return cls._instance

    @classmethod
    def get_repo_dir(cls) -> str:
        """
        Get the directory used for loading repostories.

        :return: The path to the repository directory
        """
        return cls._get_instance()._repo_path

    @classmethod
    def get_unit(cls, resource_uri: str) -> Unit:
        """
        Get a unit by its resource URI.

        :param resource_uri: The unit's resource URI
        :return: The unit, or None on error
        """
        return cls._get_instance()._get_unit(resource_uri)

    def _get_unit(self, resource_uri: str) -> Unit:
        """
        Internal implementation of get_unit().
        """
        unit = Unit(
            resource_uri=resource_uri,
        )

        statements = self._get_statements(
            self._repos,
            lambda subj, pred, obj: str(subj) == resource_uri,
        )

        for (subject, predicate, obj) in statements:
            if predicate == QUDT.SYMBOL:
                unit.symbol = str(obj)
            elif predicate == QUDT.ABBREVIATION:
                unit.abbreviation = str(obj)
            elif predicate == QUDT.CONVERSION_OFFSET:
                unit.multiplier.offset = float(obj)
            elif predicate == QUDT.CONVERSION_MULTIPLIER:
                unit.multiplier.multiplier = float(obj)
            elif predicate == RDFS.LABEL:
                unit.label = str(obj)
            elif predicate == RDF.TYPE:
                type_uri = str(obj)
                if not self._should_be_ignored(type_uri):
                    unit.type_uri = type_uri

        return unit

    @classmethod
    def find_units(cls, abbreviation: str) -> list:
        """
        Get units by their abbreviation.

        :param abbreviation: The unit abbreviation, e.g. 'nM'
        :return: The list of units, or empty if no units matched the symbol
        """
        return cls._get_instance()._find_units(abbreviation)

    def _find_units(self, abbreviation: str) -> list:
        """
        Internal implementation of find_uris()
        """
        found_units = []

        statements = self._get_statements(
            self._repos,
            lambda subj, pred, o: str(pred) == QUDT.ABBREVIATION and str(o) == abbreviation,
        )

        for (subject, predicate, obj) in statements:
            type_uri = subject
            found_units.append(self._get_unit(type_uri))

        return found_units

    @classmethod
    def get_uris(cls, type_uri: str) -> list:
        """
        Return a list of unit URIs with the given unit type.

        :param type_uri: The URI of the unit type, e.g. 'http://qudt.org/schema/qudt#TemperatureUnit'
        :return: The list of units, or empty if none match the specified type
        """
        return cls._get_instance()._get_uris(type_uri)

    def _get_uris(self, type_uri: str) -> list:
        """
        Internal implementation of get_uris()
        """
        statements = self._get_statements(
            self._repos,
            lambda subj, pred, o: str(o) == type_uri,
        )

        return [subj for (subj, pred, o) in statements]

    def _read_repo(self, file_name) -> rdflib.Graph:
        """
        Helper function to load the RDF triplet repository.

        :param file_name: The path to the repo
        :return: The loaded graph object
        """
        repo_path = os.path.join(self._repo_path, file_name)

        return OntologyReader.read(repo_path)

    @staticmethod
    def _get_statements(repos, triplet_test):
        """
        Get the statements of the given repos that match the provided resource URI.

        :param repos: The ontology repositories
        :param resource_uri: The resource to locate
        :return: The matching statements
        """
        statements = []

        for repo in repos:
            for (subject, predicate, obj) in repo:
                if triplet_test(subject, predicate, obj):
                    statements.append((str(subject), str(predicate), obj))

        return statements

    @staticmethod
    def _should_be_ignored(type_uri: str) -> bool:
        """
        Check if a statement should be ignored when constructing units.

        :param type_uri: The predicate type
        :return: True if the statement should be ignored, False otherwise
        """
        # Accept anything outside the QUDT namespace
        if not type_uri.startswith(QUDT.namespace):
            return False

        if type_uri in [
            QUDT.SI_DERIVED_UNIT,
            QUDT.SI_BASE_UNIT,
            QUDT.SI_UNIT,
            QUDT.DERIVED_UNIT,
            QUDT.NOT_USED_WITH_SI_UNIT,
            QUDT.USED_WITH_SI_UNIT,
        ]:
            return True

        # Everything else is fine too
        return False
