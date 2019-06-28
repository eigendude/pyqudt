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
#################################################################################

from qudt.ontology.OntologyUtils import OntologyUtils


OntologyUtils.register_namespace('qudt', 'http://qudt.org/schema/qudt#')


class QUDT(object):
    namespace = OntologyUtils.get_namespace('qudt')

    SYMBOL = OntologyUtils.get_uri('qudt', 'symbol')
    ABBREVIATION = OntologyUtils.get_uri('qudt', 'abbreviation')
    CONVERSION_OFFSET = OntologyUtils.get_uri('qudt', 'conversionOffset')
    CONVERSION_MULTIPLIER = OntologyUtils.get_uri('qudt', 'conversionMultiplier')

    SI_UNIT = OntologyUtils.get_uri('qudt', 'SIUnit')
    SI_BASE_UNIT = OntologyUtils.get_uri('qudt', 'SIBaseUnit')
    SI_DERIVED_UNIT = OntologyUtils.get_uri('qudt', 'SIDerivedUnit')
    DERIVED_UNIT = OntologyUtils.get_uri('qudt', 'DerivedUnit')
    NOT_USED_WITH_SI_UNIT = OntologyUtils.get_uri('qudt', 'NotUsedWithSIUnit')
    USED_WITH_SI_UNIT = OntologyUtils.get_uri('qudt', 'UsedWithSIUnit')
