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
from qudt.ontology.UnitFactory import UnitFactory

import os
import unittest

ONTOLOGY_FILE = 'ops.ttl'


class OntologyReaderTest(unittest.TestCase):
    def test_unit_ontology(self):
        schema_path = UnitFactory.get_repo_dir()

        repo_path = os.path.join(schema_path, ONTOLOGY_FILE)

        repos = OntologyReader.read(repo_path)

        self.assertGreaterEqual(len(repos), 1)


if __name__ == '__main__':
    unittest.main()
