boatd - sailing boat daemon 
===========================

Experimental robotic sailing boat daemon.

[![BuildStatus](https://travis-ci.org/boatd/boatd.png?branch=master)](https://travis-ci.org/boatd/boatd)
[![CoverageStatus](https://coveralls.io/repos/boatd/boatd/badge.png?branch=master)](https://coveralls.io/r/boatd/boatd?branch=master)

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

Installing dependencies
-----------------------

Boatd is tested on Python 2.7, 3.2 and 3.3.

### pip

```bash
$ pip install -r requirements.txt
```

### Debian

On any Debian based distribution:

```bash
$ apt-get install python-yaml
```

### Fedora

```bash
$ yum install PyYAML
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
..........
----------------------------------------------------------------------
Ran 30 tests in 0.118s

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
    - Returns: `0`-`360`
  - `@driver.wind` - Return the direction the wind is blowing, relative to the world.
    - Returns: `0`-`360`
  - `@driver.position` - Return a tuple containing the current latitude and longitude
    of the boat, in that order.
    - Returns: (`-90`-`+90`, `-180`-`+180`)
  - `@driver.rudder` - Set the boat's rudder to `angle`  degrees relative to the
    boat.
    - Arguments:
      - `angle`: Float, `-90`-`+90`
    - Returns: True if successful
  - `@driver.sail` - Similarly to `rudder`, set the sail to `angle` degrees
    relative to the boat.
    - Arguments:
      - `angle`: Float, `-90`-`+90`
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
