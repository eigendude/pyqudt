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

import os

from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import rdflib

from qudt.ontology.ontology_reader import OntologyReader
from qudt.ontology.qudt import QUDT
from qudt.ontology.rdf import RDF
from qudt.ontology.rdfs import RDFS
from qudt.unit import Unit


# Type definitions
Statement = Tuple[str, str, rdflib.term.Identifier]
Predicate = Callable[[str, str, rdflib.term.Identifier], bool]


# The package containing the RDF triplet repositories
REPO_PACKAGE_NAME = 'resources'

# The RDF triplet repositories to load
REPO_FILES = [
    'openphacts.jsonld',
    'unit.jsonld',
    'contrib.jsonld',
]


class UnitFactory(object):
    """
    A factory for creating units of measurement.
    """

    _instance: Optional['UnitFactory'] = None

    def __init__(self):
        """
        Create an instance of the unit factory and load the RDF triplet
        repositories.
        """
        # Get the path to this package
        package_path = os.path.dirname(os.path.realpath(__file__))

        # Get the path to the repository files
        self._repo_path: str = os.path.join(package_path, REPO_PACKAGE_NAME)

        # Load the repositories
        self._repos: List[rdflib.Graph] = list()
        for repo_file in REPO_FILES:
            try:
                self._repos.append(self._read_repo(repo_file))
            except FileNotFoundError:
                pass

    @classmethod
    def _get_instance(cls) -> 'UnitFactory':
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
        Get the directory used for loading repositories.

        :return: The path to the repository directory
        """
        return cls._get_instance()._repo_path

    @classmethod
    def load_repo(cls, repo_file: str) -> int:
        """
        Loads the specified RDF triplet repo using rdflib.

        If the repo's file does not exist, this function has no effect and
        returns 0.

        :param repo_file: The path to the RDF triplet repo
        :return: The number of triplets loaded, or 0 if the file doesn't exist
        """
        # Load the repository
        try:
            repo = OntologyReader.read(repo_file)
        except FileNotFoundError:
            return 0

        # Store the results
        if repo:
            cls._get_instance()._repos.append(repo)

        # Return the number of triplets read into the graph
        return len(repo)

    @classmethod
    def get_unit(cls, resource_iri: str) -> Unit:
        """
        Get a unit by its resource IRI.

        :param resource_iri: The unit's resource IRI
        :return: The unit, or None on error
        """
        return cls._get_instance()._get_unit(resource_iri)

    def _get_unit(self, resource_iri: str) -> Unit:
        """
        Internal implementation of get_unit().
        """
        unit = Unit(
            resource_iri=resource_iri,
        )

        statements: List[Statement] = self._get_statements(
            self._repos,
            lambda subj, pred, obj: str(subj) == resource_iri,
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
                type_iri = str(obj)
                if not self._should_be_ignored(type_iri):
                    unit.type_iri = type_iri

        return unit

    @classmethod
    def find_units(cls, abbreviation: str) -> List[Unit]:
        """
        Get units by their abbreviation.

        :param abbreviation: The unit abbreviation, e.g. 'nM'
        :return: The list of units, or empty if no units matched the abbreviation
        """
        return cls._get_instance()._find_units(abbreviation)

    def _find_units(self, abbreviation: str) -> List[Unit]:
        """
        Internal implementation of find_units()
        """
        found_units: List[Unit] = list()

        statements: List[Statement] = self._get_statements(
            self._repos,
            lambda subj, pred, o: str(pred) == QUDT.ABBREVIATION
            and str(o) == abbreviation,
        )

        for (subject, predicate, obj) in statements:
            type_iri = subject
            found_units.append(self._get_unit(type_iri))

        return found_units

    @classmethod
    def get_iris(cls, type_iri: str) -> List[str]:
        """
        Return a list of unit IRIs with the given unit type.

        :param type_iri: The IRI of the unit type, e.g. 'http://qudt.org/schema/qudt#TemperatureUnit'
        :return: The list of units, or empty if none match the specified type
        """
        return cls._get_instance()._get_iris(type_iri)

    def _get_iris(self, type_iri: str) -> List[str]:
        """
        Internal implementation of get_iris()
        """
        statements: List[Statement] = self._get_statements(
            self._repos,
            lambda subj, pred, o: str(o) == type_iri,
        )

        return [subj for (subj, pred, o) in statements]

    def _read_repo(self, file_name: str) -> rdflib.Graph:
        """
        Helper function to load the RDF triplet repository.

        :param file_name: The path to the repo
        :return: The loaded graph object
        """
        repo_path = os.path.join(self._repo_path, file_name)

        return OntologyReader.read(repo_path)

    @staticmethod
    def _get_statements(
        repos: List[rdflib.Graph], triplet_test: Predicate
    ) -> List[Statement]:
        """
        Get the statements of the given repos that satisfy the provided lambda.

        :param repos: The ontology repositories
        :param triplet_test: The lambda to invoke per statement
        :return: The matching statements
        """
        statements: List[Statement] = list()

        for repo in repos:
            for (subject, predicate, obj) in repo:
                if triplet_test(subject, predicate, obj):
                    statements.append((str(subject), str(predicate), obj))

        return statements

    @staticmethod
    def _should_be_ignored(type_iri: str) -> bool:
        """
        Check if a statement should be ignored when constructing units.

        :param type_iri: The predicate type
        :return: True if the statement should be ignored, False otherwise
        """
        # Accept anything outside the QUDT namespace
        if not type_iri.startswith(QUDT.namespace):
            return False

        if type_iri in [
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
