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


class ConcentrationUnit(object):
    """ """

    MOLE_PER_CUBIC_METER: Unit = UnitFactory.get_unit(
        'http://qudt.org/vocab/unit#MolePerCubicMeter'
    )

    MOLAR: Unit = UnitFactory.get_unit('http://www.openphacts.org/units/Molar')
    MILLIMOLAR: Unit = UnitFactory.get_unit(
        'http://www.openphacts.org/units/Millimolar'
    )
    NANOMOLAR: Unit = UnitFactory.get_unit('http://www.openphacts.org/units/Nanomolar')
    MICROMOLAR: Unit = UnitFactory.get_unit(
        'http://www.openphacts.org/units/Micromolar'
    )

    GRAM_PER_LITER: Unit = UnitFactory.get_unit(
        'http://www.openphacts.org/units/GramPerLiter'
    )
    MICROGRAM_PER_MILLILITER: Unit = UnitFactory.get_unit(
        'http://www.openphacts.org/units/MicrogramPerMilliliter'
    )
    PICOGRAM_PER_MILLILITER: Unit = UnitFactory.get_unit(
        'http://www.openphacts.org/units/PicogramPerMilliliter'
    )
