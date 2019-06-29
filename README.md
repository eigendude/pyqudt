# Introduction

pyqudt is a Python library for working with QUDT units and convertions between them. It is based on jQUDT, a similar Java library.

QUDT is "Quantities, Units, Dimensions and Data Types in OWL and XML".

    http://www.qudt.org

QUDT is a CC-SA-BY project by NASA Ames Research Center and TopQuadrant, Inc.

License of this Python library: 3-clause BSD ("New BSD License")

# Status

The package is relatively complete and test cases cover most code. Version 1.0.0 has been released.

# Quick demo

Keep in mind, these conversions are purely derived from data in the QUDT ontology.

Source:

```python
from qudt import Quantity
from qudt.units import ConcentrationUnit
from qudt.units import TemperatureUnit

obs = Quantity(0.1, ConcentrationUnit.MICROMOLAR)
print(f'{obs} = {obs.convert_to(ConcentrationUnit.NANOMOLAR)}')

temp = Quantity(20, TemperatureUnit.CELSIUS)
print(f'{temp} = {temp.convert_to(TemperatureUnit.KELVIN)}')
```

Output

````
0.1 μM = 100.00000000000001 nM
20 degC = 293.15 K
````
