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

from qudt.units.concentration import ConcentrationUnit
from qudt.quantity import Quantity

import unittest


class NanomolarTest(unittest.TestCase):
    def test_molar_conversion(self) -> None:
        obs = Quantity(0.1, ConcentrationUnit.MICROMOLAR)
        obs2 = obs.convert_to(ConcentrationUnit.NANOMOLAR)

        self.assertEqual(ConcentrationUnit.NANOMOLAR, obs2.unit)
        self.assertAlmostEqual(100, obs2.value)

    def test_compare_to_mole_per_cubic_meter(self) -> None:
        obs = Quantity(1.0, ConcentrationUnit.NANOMOLAR)
        obs2 = obs.convert_to(ConcentrationUnit.MOLE_PER_CUBIC_METER)

        self.assertEqual(ConcentrationUnit.MOLE_PER_CUBIC_METER, obs2.unit)
        self.assertAlmostEqual(1.0e-6, obs2.value)


if __name__ == '__main__':
    unittest.main()
