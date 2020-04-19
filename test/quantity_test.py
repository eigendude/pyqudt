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

from qudt.quantity import Quantity
from qudt.units.temperature import TemperatureUnit

import unittest


class QuantityTest(unittest.TestCase):
    def test_constructor_null_unit(self) -> None:
        quantity = Quantity(0.1, None)

        self.assertAlmostEqual(0.1, quantity.value)
        self.assertFalse(quantity.unit)

    def test_constructor(self) -> None:
        quantity = Quantity(0.1, TemperatureUnit.CELSIUS)

        self.assertAlmostEqual(0.1, quantity.value)
        self.assertEqual(TemperatureUnit.CELSIUS, quantity.unit)

    def test_jsonld(self) -> None:
        quantity = Quantity(0.1, TemperatureUnit.CELSIUS)

        self.assertTrue(quantity.jsonld())

    def test_serialization(self) -> None:
        # TODO: Improve serialization test

        quantity = Quantity(0.1, TemperatureUnit.CELSIUS)

        self.assertTrue(quantity.serialize())

    def test_deserialize(self) -> None:
        doc = {
            "@type": "http://qudt.org/schema/qudt#QuantityValue",
            "http://qudt.org/schema/qudt#numericValue": 1,
            "http://qudt.org/schema/qudt#unit": "http://qudt.org/vocab/unit#Unitless"
        }

        quantity = Quantity.from_jsonld(doc)

        self.assertEqual(quantity.value, 1)

        assert quantity.unit is not None

        self.assertEqual(quantity.unit.resource_iri, "http://qudt.org/vocab/unit#Unitless")
        self.assertEqual(quantity.unit.type_iri, 'http://qudt.org/schema/qudt#DimensionlessUnit')


if __name__ == '__main__':
    unittest.main()
