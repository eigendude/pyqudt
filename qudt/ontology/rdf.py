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
################################################################################

from qudt.ontology.ontology_utils import OntologyUtils


OntologyUtils.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')


class RDF(object):
    namespace = OntologyUtils.get_namespace('rdf')

    TYPE = OntologyUtils.get_iri('rdf', 'type')
