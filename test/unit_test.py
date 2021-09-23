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

import unittest

from qudt.unit import Unit


class UnitTest(unittest.TestCase):
    def test_resource_iri(self) -> None:
        resource_iri = 'http://qudt.org/vocab/unit#Kelvin'
        unit = Unit(resource_iri=resource_iri)

        self.assertEqual(resource_iri, unit.resource_iri)

    def test_equals(self) -> None:
        resource_iri1 = 'http://qudt.org/vocab/unit#Kelvin'
        unit1 = Unit(resource_iri=resource_iri1)

        resource_iri2 = 'http://qudt.org/vocab/unit#Kelvin'
        unit2 = Unit(resource_iri=resource_iri2)

        self.assertEqual(unit1, unit2)

    def test_type(self) -> None:
        resource_iri = 'http://qudt.org/vocab/unit#Kelvin'
        unit = Unit(resource_iri=resource_iri)

        self.assertFalse(unit.type_iri)

        unit.type_iri = resource_iri

        self.assertTrue(unit.type_iri)
        self.assertEqual(resource_iri, unit.type_iri)

    def test_label(self) -> None:
        resource_iri = 'http://qudt.org/vocab/unit#Kelvin'
        label = 'nanomolar'

        unit = Unit(resource_iri=resource_iri)

        self.assertFalse(unit.label)

        unit.label = label

        self.assertTrue(unit.label)
        self.assertEqual(label, unit.label)

    def test_abbreviation(self) -> None:
        resource_iri = 'http://qudt.org/vocab/unit#Kelvin'
        abbreviation = 'nM'

        unit = Unit(resource_iri=resource_iri)

        self.assertFalse(unit.abbreviation)

        unit.abbreviation = abbreviation

        self.assertTrue(unit.abbreviation)
        self.assertEqual(abbreviation, unit.abbreviation)

    def test_symbol(self) -> None:
        resource_iri = 'http://qudt.org/vocab/unit#Kelvin'
        symbol = 'K'

        unit = Unit(resource_iri=resource_iri)

        self.assertFalse(unit.symbol)

        unit.symbol = symbol

        self.assertTrue(unit.symbol)
        self.assertEqual(symbol, unit.symbol)


if __name__ == '__main__':
    unittest.main()
