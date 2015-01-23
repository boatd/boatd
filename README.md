boatd - sailing boat daemon 
===========================

Experimental robotic sailing boat daemon.

[![PyPIVersion](https://pypip.in/v/boatd/badge.png?style=flat)](https://pypi.python.org/pypi/boatd)
[![BuildStatus](https://travis-ci.org/boatd/boatd.png?branch=master)](https://travis-ci.org/boatd/boatd)
[![CoverageStatus](https://coveralls.io/repos/boatd/boatd/badge.png?branch=master&style=flat)](https://coveralls.io/r/boatd/boatd?branch=master)

General architecture
-----------

Boatd is designed to be the manager for a boat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using boatd:

  - the __driver__ interfaces with the particular set of hardware in the boat.

  - the __behaviour__ performs a set of actions to make the boat do a
    particular task. The API available for these scripts is supposed to be
    declarative, with the idea that for any boat with a driver written, any
    behavour script will work.

```
           boatd
             |
        -----------
       |           |
     driver     behaviour
       |
  boat hardware
```

Installing
----------

Boatd is tested on Python 2.7, 3.2 and 3.3.

### From PyPi (recommended)

```bash
$ pip install boatd
```

### Debian

On any Debian based distribution:

```bash
$ apt-get install python-yaml
$ python setup.py install
```

### Fedora

```bash
$ yum install PyYAML
$ python setup.py install
```

Testing
-------

To run tests, install nose

```bash
$ pip install nose
```

and run `nosetests`. If all the tests pass, the output should be similar to:

```bash
$ nosetests
..........................................
----------------------------------------------------------------------
Ran 42 tests in 1.064s

OK
```

The current test results from the head of the `master` branch can be found
[here](https://travis-ci.org/boatd/boatd).

Drivers
-------

### Driver basics

Boatd drivers are implemented as a simple python module. When a behaviour
script requires information about the current state of the boat or needs to
send a command to some hardware, boatd runs one of the functions in the driver.

Drivers should implement functions decorated by the following:

  - `@driver.heading` - Return the heading of the boat in degrees, relative to the
    world.
    - Returns: 0-360
  - `@driver.wind_position` - Return the direction the wind is blowing, relative to the world.
    - Returns: 0-360
  - `@driver.wind_speed` - Return the speed the wind is blowing in knots.
    - Returns: >= 0
  - `@driver.position` - Return a tuple containing the current latitude and longitude
    of the boat, in that order.
    - Returns: (-90 - +90, -180 - +180)
  - `@driver.rudder` - Set the boat's rudder to `angle`  degrees relative to the
    boat.
    - Takes the arguments:
      - `angle`: Float, -90 - +90
    - Returns: True if successful
  - `@driver.sail` - Similarly to `rudder`, set the sail to `angle` degrees
    relative to the boat.
    - Takes the arguments:
      - `angle`: Float, -90 - +90
    - Returns: True if successful

These functions can have any name, but are marked for use and registered with
boatd using decorators.

Example, only implementing `heading`:

```python
import boatd
driver = boatd.Driver()

@driver.heading
def get_heading():
    return some_compass.bearing()
```

### Custom handlers

If the behaviour script needs to run some other function in the driver, a
handler can be registered using `driver.handler(name)`

For example:

```python
@driver.handler('pony')
def example_handler():
    return something
```

This can then be used as any other function in a behaviour client.

License
-------

Copyright (c) 2013-2014 Louis Taylor <kragniz@gmail.com>

Boatd is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

See [COPYING](COPYING) for more information.
