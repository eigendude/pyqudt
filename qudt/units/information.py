################################################################################
#
#  Copyright (C) 2020 Garrett Brown
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


class InformationUnit(object):
    """ """

    BYTE: Unit = UnitFactory.get_unit('http://qudt.org/vocab/unit#Byte')
    KILOBYTE: Unit = UnitFactory.get_unit('http://aclima.io/schema/1.0/Kilobyte')
    MEGABYTE: Unit = UnitFactory.get_unit('http://aclima.io/schema/1.0/Megabyte')
    GIGABYTE: Unit = UnitFactory.get_unit('http://aclima.io/schema/1.0/Gigabyte')
