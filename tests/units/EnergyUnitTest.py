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

from qudt.units.EnergyUnit import EnergyUnit
from qudt import Quantity

import unittest


class EnergyUnitTest(unittest.TestCase):
    def test_electron_volt(self):
        temp = Quantity(-23.5, EnergyUnit.EV)

        self.assertEqual("eV", temp.unit.abbreviation)


if __name__ == '__main__':
    unittest.main()
