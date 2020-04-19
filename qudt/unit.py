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
from qudt.ontology.qudt import QUDT
from qudt.ontology.rdfs import RDFS

import dataclasses
from typing import Any
from typing import ClassVar
from typing import Dict


@dataclasses.dataclass(repr=False)
class Unit(BaseModel):
    """
    A unit of measurement.
    """
    resource_iri: str
    label: str = dataclasses.field(default_factory=str)
    abbreviation: str = dataclasses.field(default_factory=str)
    symbol: str = dataclasses.field(default_factory=str)
    type_iri: str = dataclasses.field(default_factory=str)
    offset: float = dataclasses.field(default=0.0)
    multiplier: float = dataclasses.field(default=1.0)

    def __repr__(self) -> str:
        return str(self.abbreviation)

    ############################################################################
    # Serialization
    ############################################################################

    _SCHEMA: ClassVar[Dict[str, Any]] = {
        'resource_iri': '@id',
        'label': RDFS.LABEL,
        'abbreviation': QUDT.ABBREVIATION,
        'symbol': QUDT.SYMBOL,
        'type_iri': '@type',
        'offset': QUDT.CONVERSION_OFFSET,
        'multiplier': QUDT.CONVERSION_MULTIPLIER,
    }

    ############################################################################
    # Deserialization
    ############################################################################

    @staticmethod
    def from_jsonld(json_document: Dict[str, Any]) -> 'Unit':
        """
        Deserialize data model.
        """
        return Unit(
            resource_iri=json_document['@id'],
            label=json_document.get(RDFS.LABEL, ''),
            abbreviation=json_document.get(QUDT.ABBREVIATION, ''),
            symbol=json_document.get(QUDT.SYMBOL, ''),
            type_iri=json_document.get('@type', ''),
            offset=json_document.get(QUDT.CONVERSION_OFFSET, 0.0),
            multiplier=json_document.get(QUDT.CONVERSION_MULTIPLIER, 1.0)
        )
