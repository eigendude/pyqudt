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

from qudt.contrib.models import BaseModel
from qudt.ontology.qudt import QUDT
from qudt.unit import Unit
from qudt.units.dimensionless import DimensionlessUnit

import dataclasses


_CONTEXT = {
    '@type': QUDT.QUANTITY_VALUE,
    'value': QUDT.NUMERIC_VALUE,
    'unit': [QUDT.UNIT, lambda unit: unit.resource_iri],
}


@dataclasses.dataclass(repr=False)
class Quantity(BaseModel):
    """
    A quantity with a value and a unit.
    """
    value: float
    unit: Unit = DimensionlessUnit.UNITLESS

    def __post_init__(self) -> None:
        BaseModel.__post_init__(self, _CONTEXT)
        #self._post_init(_CONTEXT)

    def convert_to(self, unit: Unit) -> 'Quantity':
        """
        Converts the quantity's value to the specified unit of measurement.

        :param unit: The target unit
        :return: The converted quantity
        """
        if not unit:
            raise ValueError('Target unit cannot be null')

        if not self.unit:
            raise ValueError('This measurement does not have units defined')

        if self.unit == unit:
            # Nothing to be done
            return self

        if self.unit.type_iri != unit.type_iri:
            raise ValueError(
                f'The new unit does not have the same parent type '
                f'(source: {self.unit.type_iri}; target: {unit.type_iri})'
            )

        # Convert to the base unit
        base_unit_value = self.value * self.unit.multiplier + self.unit.offset

        # Convert the base unit to the new unit
        new_value = (base_unit_value - unit.offset) / unit.multiplier

        new_measurement = Quantity(
            unit=unit,
            value=new_value,
        )

        return new_measurement

    def __repr__(self) -> str:
        """
        Return a string representation of the quantity.
        """
        return f'{self.value} {self.unit}'
