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

from qudt.ontology.OntologyUtils import OntologyUtils

import unittest


OntologyUtils.register_namespace('qudt', 'http://qudt.org/schema/qudt#')


class OntologyUtilsTest(unittest.TestCase):
    def test_get_namespace(self):
        namespace = OntologyUtils.get_namespace('qudt')

        self.assertEqual('http://qudt.org/schema/qudt#', namespace)

    def test_get_uri(self):
        resource_uri = OntologyUtils.get_uri('qudt', 'symbol')

        self.assertEqual('http://qudt.org/schema/qudt#symbol', resource_uri)


if __name__ == '__main__':
    unittest.main()
