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

from qudt.units.energy import EnergyUnit
from qudt.quantity import Quantity

import unittest


class EnergyUnitTest(unittest.TestCase):
    def test_electron_volt(self) -> None:
        temp = Quantity(-23.5, EnergyUnit.EV)

        assert temp.unit is not None

        self.assertEqual("eV", temp.unit.abbreviation)

    def test_kwh_to_btu(self) -> None:
        kwh = Quantity(50, EnergyUnit.KWH)

        self.assertTrue(kwh.unit)

        btu = kwh.convert_to(EnergyUnit.BTU)
        self.assertEqual(btu.unit, EnergyUnit.BTU)
        self.assertAlmostEqual(btu.value, 170607.08, 2)


if __name__ == '__main__':
    unittest.main()
