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


OntologyUtils.register_namespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')


class RDFS(object):
    """
    The RDF Schema provides a data-modelling vocabulary for RDF data.

    Reference:

        https://www.w3.org/TR/rdf-schema/

    """

    namespace = OntologyUtils.get_namespace('rdfs')

    ############################################################################
    #
    # Properties
    #
    # The RDF Concepts and Abstract Syntax specification describes an RDF
    # property as a relation between subject resources and object resources.
    #
    # Reference:
    #
    #     https://www.w3.org/TR/rdf-schema/#ch_properties
    #
    ############################################################################

    LABEL = OntologyUtils.get_iri('rdfs', 'label')
    """
    A human-readable version of a resource's name.

    Reference:

        https://www.w3.org/TR/rdf-schema/#ch_label

    """
