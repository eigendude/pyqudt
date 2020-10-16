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

from qudt.units.temperature import TemperatureUnit
from qudt.quantity import Quantity

import unittest


class CelsiusTest(unittest.TestCase):
    def test_absolute_zero(self) -> None:
        temp = Quantity(-273.15, TemperatureUnit.CELSIUS)
        temp2 = temp.convert_to(TemperatureUnit.KELVIN)

        self.assertEqual(TemperatureUnit.KELVIN, temp2.unit)
        self.assertAlmostEqual(0.0, temp2.value)

    def test_room_temperature(self) -> None:
        temp = Quantity(20, TemperatureUnit.CELSIUS)
        temp2 = temp.convert_to(TemperatureUnit.KELVIN)

        self.assertEqual(TemperatureUnit.KELVIN, temp2.unit)
        self.assertAlmostEqual(293.15, temp2.value)

        temp_f = temp.convert_to(TemperatureUnit.FAHRENHEIT)
        self.assertEqual(TemperatureUnit.FAHRENHEIT, temp_f.unit)
        self.assertAlmostEqual(68, temp_f.value, 2)


if __name__ == '__main__':
    unittest.main()
