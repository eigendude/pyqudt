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

import dataclasses


@dataclasses.dataclass
class Multiplier(object):
    """
    A multiplier with an optional offset.
    """

    offset: float = dataclasses.field(default=0.0)
    multiplier: float = dataclasses.field(default=1.0)
