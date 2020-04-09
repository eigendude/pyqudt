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

from qudt.units.area import AreaUnit
from qudt.quantity import Quantity

import unittest


class SquareAreaTest(unittest.TestCase):
    def test_electron_volt(self) -> None:
        area = Quantity(5, AreaUnit.SQUARE_ANGSTROM)
        area2 = area.convert_to(AreaUnit.SQUARE_METER)

        self.assertAlmostEqual(0.00000000000000000005, area2.value)


if __name__ == '__main__':
    unittest.main()
