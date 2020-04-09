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

from qudt.ontology.ontology_utils import OntologyUtils

import unittest


OntologyUtils.register_namespace('qudt', 'http://qudt.org/schema/qudt#')


class OntologyUtilsTest(unittest.TestCase):
    def test_get_namespace(self) -> None:
        namespace = OntologyUtils.get_namespace('qudt')

        self.assertEqual('http://qudt.org/schema/qudt#', namespace)

    def test_get_iri(self) -> None:
        resource_iri = OntologyUtils.get_iri('qudt', 'symbol')

        self.assertEqual('http://qudt.org/schema/qudt#symbol', resource_iri)


if __name__ == '__main__':
    unittest.main()
