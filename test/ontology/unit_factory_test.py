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

from qudt.ontology.unit_factory import UnitFactory
from qudt.unit import Unit

import unittest


class UnitFactoryTest(unittest.TestCase):
    def test_get_instance(self) -> None:
        factory = UnitFactory._get_instance()

        self.assertTrue(factory)

    def test_get_unit(self) -> None:
        unit = UnitFactory.get_unit('http://qudt.org/vocab/unit#Kelvin')

        self.assertTrue(isinstance(unit, Unit))
        self.assertEqual('Kelvin', unit.label)
        self.assertEqual('K', unit.symbol)
        self.assertEqual('K', unit.abbreviation)
        self.assertEqual(1, unit.multiplier.multiplier)
        self.assertEqual(0, unit.multiplier.offset)
        self.assertEqual('http://qudt.org/schema/qudt#TemperatureUnit', unit.type_iri)

    def test_get_iris(self) -> None:
        units = UnitFactory.get_iris('http://qudt.org/schema/qudt#TemperatureUnit')

        self.assertTrue(units)
        self.assertGreaterEqual(len(units), 1)

    def test_get_open_phacts_unit(self) -> None:
        unit = UnitFactory.get_unit('http://www.openphacts.org/units/Nanomolar')

        self.assertTrue(unit)
        self.assertEqual('Nanomolar', unit.label)
        self.assertEqual('nmol/dm^3', unit.symbol)
        self.assertEqual('nM', unit.abbreviation)
        self.assertAlmostEqual(0.000001, unit.multiplier.multiplier)
        self.assertAlmostEqual(0, unit.multiplier.offset)
        self.assertEqual('http://qudt.org/schema/qudt#MolarConcentrationUnit', unit.type_iri)

    def test_get_open_phacts_unit_newer(self) -> None:
        unit = UnitFactory.get_unit('http://www.openphacts.org/units/NanogramPerMilliliter')

        self.assertTrue(unit)
        self.assertEqual('http://qudt.org/schema/qudt#MassPerVolumeUnit', unit.type_iri)

    def test_find_units(self) -> None:
        units = UnitFactory.find_units('nM')

        self.assertTrue(units)
        self.assertGreaterEqual(len(units), 1)
        self.assertEqual('http://www.openphacts.org/units/Nanomolar', units[0].resource_iri)


if __name__ == '__main__':
    unittest.main()
