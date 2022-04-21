from qudt.unit import Unit
from qudt.ontology.unit_factory import UnitFactory


class TimeUnit:
    SECOND: Unit = UnitFactory.get_qudt('SEC')
    HOUR: Unit = UnitFactory.get_qudt('HR')
