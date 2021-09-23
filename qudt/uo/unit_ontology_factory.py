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

from typing import Dict
from typing import List
from typing import Optional

from qudt.ontology.unit_factory import UnitFactory
from qudt.unit import Unit


def long_iri(shortened_iri: str) -> str:
    if shortened_iri.startswith('uo:'):
        return 'http://purl.obolibrary.org/obo/' + shortened_iri[3:]
    elif shortened_iri.startswith('ops:'):
        return 'http://www.openphacts.org/units/' + shortened_iri[4:]
    elif shortened_iri.startswith('qudt:'):
        return 'http://qudt.org/schema/qudt#' + shortened_iri[5:]

    raise ValueError(f'Invalid shortened IRI: {shortened_iri}')


class UnitOntologyFactory(object):
    """
    A class for creating units from the Unit Ontology.
    """

    uo_to_qudt: Dict[str, str] = {
        long_iri('uo:EFO_0004374'): long_iri('ops:MilligramPerDeciliter'),
        long_iri('uo:EFO_0004385'): long_iri('ops:PicogramPerMilliliter'),
        long_iri('uo:UO_0000009'): long_iri('qudt:Kilogram'),
        long_iri('uo:UO_0000010'): long_iri('qudt:SecondTime'),
        long_iri('uo:UO_0000015'): long_iri('qudt:Centimeter'),
        long_iri('uo:UO_0000016'): long_iri('qudt:Millimeter'),
        long_iri('uo:UO_0000017'): long_iri('qudt:Micrometer'),
        long_iri('uo:UO_0000018'): long_iri('ops:Nanometer'),
        long_iri('uo:UO_0000021'): long_iri('qudt:Gram'),
        long_iri('uo:UO_0000022'): long_iri('ops:Milligram'),
        long_iri('uo:UO_0000023'): long_iri('ops:Microgram'),
        long_iri('uo:UO_0000024'): long_iri('ops:Nanogram'),
        long_iri('uo:UO_0000025'): long_iri('ops:Picogram'),
        long_iri('uo:UO_0000026'): long_iri('ops:Femtogram'),
        long_iri('uo:UO_0000027'): long_iri('qudt:DegreeCelsius'),
        long_iri('uo:UO_0000028'): long_iri('qudt:Millisecond'),
        long_iri('uo:UO_0000031'): long_iri('qudt:MinuteTime'),
        long_iri('uo:UO_0000032'): long_iri('qudt:Hour'),
        long_iri('uo:UO_0000033'): long_iri('qudt:Day'),
        long_iri('uo:UO_0000039'): long_iri('qudt:Micromole'),
        long_iri('uo:UO_0000040'): long_iri('qudt:Millimole'),
        long_iri('uo:UO_0000041'): long_iri('qudt:Nanomole'),
        long_iri('uo:UO_0000042'): long_iri('qudt:Picomole'),
        long_iri('uo:UO_0000043'): long_iri('qudt:Femtomole'),
        long_iri('uo:UO_0000062'): long_iri('ops:Molar'),
        long_iri('uo:UO_0000063'): long_iri('ops:Millimolar'),
        long_iri('uo:UO_0000064'): long_iri('ops:Micromolar'),
        long_iri('uo:UO_0000065'): long_iri('ops:Nanomolar'),
        long_iri('uo:UO_0000066'): long_iri('ops:Picomolar'),
        long_iri('uo:UO_0000073'): long_iri('ops:Femtomolar'),
        long_iri('uo:UO_0000098'): long_iri('ops:Milliliter'),
        long_iri('uo:UO_0000099'): long_iri('qudt:Liter'),
        long_iri('uo:UO_0000101'): long_iri('ops:Microliter'),
        long_iri('uo:UO_0000169'): long_iri('ops:PartsPerMillion'),
        long_iri('uo:UO_0000173'): long_iri('ops:GramPerMilliliter'),
        long_iri('uo:UO_0000175'): long_iri('ops:GramPerLiter'),
        long_iri('uo:UO_0000176'): long_iri('ops:MilligramPerMilliliter'),
        long_iri('uo:UO_0000187'): long_iri('qudt:Percent'),
        long_iri('uo:UO_0000197'): long_iri('ops:LiterPerKilogram'),
        long_iri('uo:UO_0000198'): long_iri('ops:MilliliterPerKilogram'),
        long_iri('uo:UO_0000271'): long_iri('ops:MicroliterPerMinute'),
        long_iri('uo:UO_0000272'): long_iri('qudt:MillimeterOfMercury'),
        long_iri('uo:UO_0000274'): long_iri('ops:MicrogramPerMilliliter'),
        long_iri('uo:UO_0000275'): long_iri('ops:NanogramPerMilliliter'),
        long_iri('uo:UO_0000308'): long_iri('ops:MilligramPerKilogram'),
        # long_iri('uo:UO_0000311'), longIRI(''),
    }

    # Reverse the lookup table
    qudt_to_uo: Dict[str, str] = {v: k for k, v in uo_to_qudt.items()}

    @classmethod
    def get_unit(cls, resource_iri: str) -> Optional[Unit]:
        """
        Get a unit from a Unit Ontology resource IRI.

        :param resource_iri: The IRI of a resource in the Unit Ontology
        :return: The resolved unit, or None on error
        """
        mapped_iri: Optional[str] = cls.uo_to_qudt.get(resource_iri)

        if mapped_iri:
            return UnitFactory.get_unit(mapped_iri)

        return None

    @classmethod
    def get_iris(cls, type_iri: str) -> List[str]:
        """
        Return a list of unit IRIs with the given unit type.

        :param type_iri: The IRI of the unit type, e.g. 'http://qudt.org/schema/qudt#MolarConcentrationUnit'
        :return: The list of IRIs, or empty if no units match the specified type
        """
        iris: List[str] = list()

        qudt_iris: List[str] = UnitFactory.get_iris(type_iri)

        for qudt_iri in qudt_iris:
            uo_iri = cls.qudt_to_uo.get(qudt_iri)
            if uo_iri:
                iris.append(uo_iri)

        return iris
