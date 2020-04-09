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
import rdflib


class OntologyReader(object):
    """
    Class to read an RDF triplet ontology repository.
    """

    @classmethod
    def read(cls, repo_path) -> rdflib.Graph:
        """
        Read an RDF triplet repository.

        :param repo_path: The path to the RDF repository
        :return: The RDF graph, or None on error
        """
        # Get the repo format based on the path
        repo_format = cls._get_repo_format(repo_path)

        # Use a conjunctive graph to fix loading the QUDT JSON-LD repository
        # See https://github.com/RDFLib/rdflib-jsonld/issues/53
        # TODO: Fix URL
        g = rdflib.ConjunctiveGraph()
        g.parse(repo_path, format=repo_format)

        return g

    @staticmethod
    def _get_repo_format(repo_path: str) -> str:
        """
        Get the RDF format used by RDFLib based on the file's extension.

        :param repo_path: The path to the RDF repository
        :return: The repo format, or None if unknown (assumed XML by RDFLib)
        """
        _, repo_ext = os.path.splitext(repo_path)

        formats = {
            '.jsonld': 'json-ld',
            '.ttl': 'turtle'
        }

        return formats.get(repo_ext)
