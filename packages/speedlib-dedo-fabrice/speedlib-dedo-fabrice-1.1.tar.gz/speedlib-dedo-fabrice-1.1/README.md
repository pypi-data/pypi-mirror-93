# SpeedLib
A python library to operate Speed devices.

Currently only the Faller (c) 180290 models is supported. 

Example
-------
```python
from speedlib.cranes import faller
faller.init("172.17.217.217")
faller.set_speed(faller.MotorChassis, 50)
faller.step(faller.MotorChassis, faller.MotorDirectionBackward)
```
You can find more examples in the *examples* directory.

Install
-------
git clone https://github.com/CRIStAL-PADR/Speed.git

The library is in speedlib/__init__.py

Tests
-----
To starts the unit tests you can do:
```console
cd tests/
PYTHONPATH=../ python3 -m unittest
```

