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

from qudt.model import BaseModel
from qudt.model import coerce
from qudt.model import link
from qudt.ontology.qudt import QUDT
from qudt.ontology.unit import UNIT
from qudt.unit import Unit

import dataclasses
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional


@dataclasses.dataclass(repr=False)
class Quantity(BaseModel):
    """
    A quantity with a value and a unit.
    """
    value: float
    unit: Optional[Unit]

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

    ############################################################################
    # Serialization
    ############################################################################

    _SCHEMA: ClassVar[Dict[str, Any]] = {
        '@type': QUDT.QUANTITY_VALUE,
        'value': QUDT.NUMERIC_VALUE,
        'unit': coerce(QUDT.UNIT, lambda unit: link(unit.resource_iri) if unit else UNIT.UNITLESS),
    }

    ############################################################################
    # Deserialization
    ############################################################################

    @staticmethod
    def from_jsonld(jsonld_document: Dict[str, Any]) -> 'Quantity':
        """
        Deserialize data model.
        """
        from qudt.ontology.unit_factory import UnitFactory

        return Quantity(
            value=jsonld_document[QUDT.NUMERIC_VALUE],
            unit=UnitFactory.get_unit(jsonld_document.get(QUDT.UNIT, UNIT.UNITLESS))
        )
