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

from qudt.uo.unit_ontology_factory import UnitOntologyFactory
from qudt.unit import Unit

import unittest


class UnitOntologyFactoryTest(unittest.TestCase):
    def test_get_unit(self) -> None:
        unit = UnitOntologyFactory.get_unit('http://purl.obolibrary.org/obo/UO_0000013')

        assert unit is not None

        self.assertTrue(isinstance(unit, Unit))
        self.assertEqual('Mole', unit.label)
        self.assertEqual('mol', unit.symbol)
        self.assertEqual('mol', unit.abbreviation)
        self.assertEqual(1.0, unit.multiplier.multiplier)
        self.assertEqual(0, unit.multiplier.offset)
        self.assertEqual('http://qudt.org/vocab/quantitykind/AmountOfSubstance', unit.type_iri)

    def test_get_units_by_qudt_type(self) -> None:
        units = UnitOntologyFactory.get_iris('http://qudt.org/vocab/quantitykind/AmountOfSubstance')

        self.assertTrue(units)
        self.assertGreaterEqual(len(units), 1)


if __name__ == '__main__':
    unittest.main()
