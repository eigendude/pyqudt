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

from qudt import Unit

import unittest


class UnitTest(unittest.TestCase):
    def test_resource_uri(self):
        resource_uri = 'http://qudt.org/vocab/unit#Kelvin'
        unit = Unit(resource_uri=resource_uri)

        self.assertEqual(resource_uri, unit.resource_uri)

    def test_equals(self):
        resource_uri1 = 'http://qudt.org/vocab/unit#Kelvin'
        unit1 = Unit(resource_uri=resource_uri1)

        resource_uri2 = 'http://qudt.org/vocab/unit#Kelvin'
        unit2 = Unit(resource_uri=resource_uri2)

        self.assertEqual(unit1, unit2)

    def test_type(self):
        resource_uri = 'http://qudt.org/vocab/unit#Kelvin'
        unit = Unit(resource_uri=resource_uri)

        self.assertFalse(unit.type_uri)

        unit.type = resource_uri

        self.assertTrue(unit.type)
        self.assertEqual(resource_uri, unit.type)

    def test_label(self):
        resource_uri = 'http://qudt.org/vocab/unit#Kelvin'
        label = 'nanomolar'

        unit = Unit(resource_uri=resource_uri)

        self.assertFalse(unit.label)

        unit.label = label

        self.assertTrue(unit.label)
        self.assertEqual(label, unit.label)

    def test_abbreviation(self):
        resource_uri = 'http://qudt.org/vocab/unit#Kelvin'
        abbreviation = 'nM'

        unit = Unit(resource_uri=resource_uri)

        self.assertFalse(unit.abbreviation)

        unit.abbreviation = abbreviation

        self.assertTrue(unit.abbreviation)
        self.assertEqual(abbreviation, unit.abbreviation)

    def test_symbol(self):
        resource_uri = 'http://qudt.org/vocab/unit#Kelvin'
        symbol = 'K'

        unit = Unit(resource_uri=resource_uri)

        self.assertFalse(unit.symbol)

        unit.symbol = symbol

        self.assertTrue(unit.symbol)
        self.assertEqual(symbol, unit.symbol)


if __name__ == '__main__':
    unittest.main()
