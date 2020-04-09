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

from qudt.ontology.qudt import QUDT

import unittest


class QUDTTest(unittest.TestCase):
    def test_unit_ontology(self) -> None:
        symbol_iri = QUDT.SYMBOL

        self.assertTrue(symbol_iri.startswith(QUDT.namespace))


if __name__ == '__main__':
    unittest.main()
