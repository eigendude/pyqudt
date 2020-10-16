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
    @unittest.skip("TODO<open phacts>")
    def test_electron_volt(self) -> None:
        area = Quantity(5, AreaUnit.SQUARE_ANGSTROM)
        area2 = area.convert_to(AreaUnit.SQUARE_METER)

        self.assertAlmostEqual(0.00000000000000000005, area2.value)

    def test_acreage(self) -> None:
        acres = Quantity(2, AreaUnit.ACRE)
        in_m2 = acres.convert_to(AreaUnit.SQUARE_METER)

        self.assertAlmostEqual(8093.71, in_m2.value, 2)


if __name__ == '__main__':
    unittest.main()
