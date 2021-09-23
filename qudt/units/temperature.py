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

from qudt.ontology.unit_factory import UnitFactory
from qudt.unit import Unit


class TemperatureUnit(object):
    """ """

    KELVIN: Unit = UnitFactory.get_unit('http://qudt.org/vocab/unit#Kelvin')
    CELSIUS: Unit = UnitFactory.get_unit('http://qudt.org/vocab/unit#DegreeCelsius')
    FAHRENHEIT: Unit = UnitFactory.get_unit(
        'http://qudt.org/vocab/unit#DegreeFahrenheit'
    )
