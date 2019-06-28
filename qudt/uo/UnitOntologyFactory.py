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

from qudt import Unit
from qudt.ontology import UnitFactory


def long_uri(shortened_uri: str) -> str:
    if shortened_uri.startswith('uo:'):
        return 'http://purl.obolibrary.org/obo/' + shortened_uri[3:]
    elif shortened_uri.startswith('ops:'):
        return 'http://www.openphacts.org/units/' + shortened_uri[4:]
    elif shortened_uri.startswith('qudt:'):
        return 'http://qudt.org/schema/qudt#' + shortened_uri[5:]

    raise ValueError(f'Invalid shortened URI: {shortened_uri}')


class UnitOntologyFactory(object):
    """
    A class for creating units from the Unit Ontology.
    """
    uo_to_qudt = {
        long_uri('uo:EFO_0004374'): long_uri('ops:MilligramPerDeciliter'),
        long_uri('uo:EFO_0004385'): long_uri('ops:PicogramPerMilliliter'),
        long_uri('uo:UO_0000009'): long_uri('qudt:Kilogram'),
        long_uri('uo:UO_0000010'): long_uri('qudt:SecondTime'),
        long_uri('uo:UO_0000015'): long_uri('qudt:Centimeter'),
        long_uri('uo:UO_0000016'): long_uri('qudt:Millimeter'),
        long_uri('uo:UO_0000017'): long_uri('qudt:Micrometer'),
        long_uri('uo:UO_0000018'): long_uri('ops:Nanometer'),
        long_uri('uo:UO_0000021'): long_uri('qudt:Gram'),
        long_uri('uo:UO_0000022'): long_uri('ops:Milligram'),
        long_uri('uo:UO_0000023'): long_uri('ops:Microgram'),
        long_uri('uo:UO_0000024'): long_uri('ops:Nanogram'),
        long_uri('uo:UO_0000025'): long_uri('ops:Picogram'),
        long_uri('uo:UO_0000026'): long_uri('ops:Femtogram'),
        long_uri('uo:UO_0000027'): long_uri('qudt:DegreeCelsius'),
        long_uri('uo:UO_0000028'): long_uri('qudt:Millisecond'),
        long_uri('uo:UO_0000031'): long_uri('qudt:MinuteTime'),
        long_uri('uo:UO_0000032'): long_uri('qudt:Hour'),
        long_uri('uo:UO_0000033'): long_uri('qudt:Day'),
        long_uri('uo:UO_0000039'): long_uri('qudt:Micromole'),
        long_uri('uo:UO_0000040'): long_uri('qudt:Millimole'),
        long_uri('uo:UO_0000041'): long_uri('qudt:Nanomole'),
        long_uri('uo:UO_0000042'): long_uri('qudt:Picomole'),
        long_uri('uo:UO_0000043'): long_uri('qudt:Femtomole'),
        long_uri('uo:UO_0000062'): long_uri('ops:Molar'),
        long_uri('uo:UO_0000063'): long_uri('ops:Millimolar'),
        long_uri('uo:UO_0000064'): long_uri('ops:Micromolar'),
        long_uri('uo:UO_0000065'): long_uri('ops:Nanomolar'),
        long_uri('uo:UO_0000066'): long_uri('ops:Picomolar'),
        long_uri('uo:UO_0000073'): long_uri('ops:Femtomolar'),
        long_uri('uo:UO_0000098'): long_uri('ops:Milliliter'),
        long_uri('uo:UO_0000099'): long_uri('qudt:Liter'),
        long_uri('uo:UO_0000101'): long_uri('ops:Microliter'),
        long_uri('uo:UO_0000169'): long_uri('ops:PartsPerMillion'),
        long_uri('uo:UO_0000173'): long_uri('ops:GramPerMilliliter'),
        long_uri('uo:UO_0000175'): long_uri('ops:GramPerLiter'),
        long_uri('uo:UO_0000176'): long_uri('ops:MilligramPerMilliliter'),
        long_uri('uo:UO_0000187'): long_uri('qudt:Percent'),
        long_uri('uo:UO_0000197'): long_uri('ops:LiterPerKilogram'),
        long_uri('uo:UO_0000198'): long_uri('ops:MilliliterPerKilogram'),
        long_uri('uo:UO_0000271'): long_uri('ops:MicroliterPerMinute'),
        long_uri('uo:UO_0000272'): long_uri('qudt:MillimeterOfMercury'),
        long_uri('uo:UO_0000274'): long_uri('ops:MicrogramPerMilliliter'),
        long_uri('uo:UO_0000275'): long_uri('ops:NanogramPerMilliliter'),
        long_uri('uo:UO_0000308'): long_uri('ops:MilligramPerKilogram'),
        #long_uri('uo:UO_0000311'), longURI(''),
    }

    # Reverse the lookup table
    qudt_to_uo = {
        v: k for k, v in uo_to_qudt.items()
    }

    @classmethod
    def get_unit(cls, resource_uri: str) -> Unit:
        """
        Get a unit from a Unit Ontology resource URI.

        :param resource_uri: The URI of a resource in the Unit Ontology
        :return: The resoluved unit, or None on error
        """
        mapped_uri = cls.uo_to_qudt.get(resource_uri)

        if mapped_uri:
            return UnitFactory.get_unit(mapped_uri)

        return None

    @classmethod
    def get_uris(cls, type_uri: str) -> list:
        """
        Return a list of unit URIs with the given unit type.

        :param type_uri: The URI of the unit type, e.g. 'http://qudt.org/schema/qudt#MolarConcentrationUnit'
        :return: The list of URIs, or empty if no units match the specified type
        """
        uris = []

        qudt_uris = UnitFactory.get_uris(type_uri)

        for qudt_uri in qudt_uris:
            uo_uri = cls.qudt_to_uo.get(qudt_uri)
            if uo_uri:
                uris.append(uo_uri)

        return uris
