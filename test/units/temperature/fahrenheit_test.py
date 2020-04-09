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


class FahrenheitTest(unittest.TestCase):
    def test_twenty_degrees(self) -> None:
        temp = Quantity(20, TemperatureUnit.CELSIUS)
        temp2 = temp.convert_to(TemperatureUnit.FAHRENHEIT)

        self.assertEqual(TemperatureUnit.FAHRENHEIT, temp2.unit)
        self.assertAlmostEqual(68, round(temp2.value, 2))

    def test_minus_fourty(self) -> None:
        temp = Quantity(-40, TemperatureUnit.CELSIUS)
        temp2 = temp.convert_to(TemperatureUnit.FAHRENHEIT)

        self.assertEqual(TemperatureUnit.FAHRENHEIT, temp2.unit)
        self.assertAlmostEqual(-40, round(temp2.value, 2))


if __name__ == '__main__':
    unittest.main()
