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

from qudt.contrib.meta import alias
from qudt.contrib.models import BaseModel
from qudt.ontology.qudt import QUDT
from qudt.ontology.rdfs import RDFS

class Unit(BaseModel):
    """
    A unit of measurement.
    """
    resource_iri: str
    label: str = alias(RDFS.LABEL, '')
    abbreviation: str = alias(QUDT.ABBREVIATION, '')
    symbol: str = alias(QUDT.SYMBOL, '')
    type_iri: str = ''  # TODO alias('@type', '')
    offset: float = alias(QUDT.CONVERSION_OFFSET, 0.0)
    multiplier: float = alias(QUDT.CONVERSION_MULTIPLIER, 1.0)

    def __repr__(self) -> str:
        return str(self.abbreviation)
