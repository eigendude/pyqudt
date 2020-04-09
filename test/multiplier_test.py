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

from qudt.multiplier import Multiplier

import unittest


class MultiplierTest(unittest.TestCase):
    def test_constructor_null_unit(self):
        multiplier = Multiplier(0.1, 0.2)

        self.assertAlmostEqual(0.1, multiplier.offset)
        self.assertAlmostEqual(0.2, multiplier.multiplier)


if __name__ == '__main__':
    unittest.main()
