===========================
boatd - sailing boat daemon 
===========================

Experimental robotic sailing boat daemon.

.. image:: https://img.shields.io/pypi/v/boatd.svg
    :target: https://pypi.python.org/pypi/boatd

.. image:: https://img.shields.io/travis/boatd/boatd.svg
    :target: https://travis-ci.org/boatd/boatd

.. image:: https://img.shields.io/coveralls/jekyll/jekyll/master.svg
    :target: https://coveralls.io/r/boatd/bocatd?branch=master


General architecture
====================

Boatd is designed to be the manager for a boat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using boatd:

- the *driver* interfaces with the particular set of hardware in the boat.

- the *behaviour* performs a set of actions to make the boat do a
  particular task. The API available for these scripts is supposed to be
  declarative, with the idea that for any boat with a driver written, any
  behavour script will work.

.. code::

             boatd
               |
          -----------
         |           |
       driver     behaviour
         |
    boat hardware


Installing
==========

Boatd is tested on Python 2.7 and 3.4.

From PyPi (recommended)
-----------------------

.. code:: bash

    $ pip install boatd


Debian
------

On any Debian based distribution:

.. code:: bash

    $ apt-get install python-yaml
    $ python setup.py install

Fedora
------

.. code:: bash

    $ yum install PyYAML
    $ python setup.py install


Running boatd
=============

.. code:: bash

    $ boatd --help
    usage: boatd [-h] [CONFIG FILE]

    Experimental robotic sailing boat daemon.

    positional arguments:
      CONFIG FILE  a path to a configuration file

      optional arguments:
        -h, --help   show this help message and exit

After you have installed boat, it can be run with ``$ boatd``.

Output will be similar to:

.. code:: bash

    $ boatd
    [15:43:55] loaded function heading as "heading"
    [15:43:55] loaded function get_wind as "wind_direction"
    [15:43:55] loaded function get_wind_speed as "wind_speed"
    [15:43:55] loaded function position as "position"
    [15:43:55] loaded function rudder as "rudder"
    [15:43:55] loaded function sail as "sail"
    [15:43:55] loaded driver from example/basic_driver.py

The original aim was this command would also run your behaviour directly after
startup, but this functionality is not yet implemented (see `the issue
<https://github.com/boatd/boatd/issues/1>`_). After boatd is running, you should
run your behaviour manually.

If you would like to use a different config file in a different location, pass
the path as an argument to ``boatd``. For example, ``$ boatd /etc/boatd/fancy-conf.yaml``.


Using the boatd API
===================

Boatd's main method of interaction is via the JSON API.

``/``
-----

- ``GET``

  Returns the current status and version of boatd. Example output:

  .. code:: json

      {
         "boatd": {
           "version": 1.1
         }
      }


``/boat``
---------

- ``GET``

  Returns attributes about the current state of the boat. Example output:

  .. code:: json

      {
        "active": false,
        "position": [2.343443, null],
        "heading": 2.43,
        "wind": {
          "direction": 8.42,
          "speed": 25
        }
      }


``wind``
--------

- ``GET``

  Returns properties of the wind. Example output:

  .. code:: json

    {
      "direction": 8.42,
      "speed": 25
    }

Drivers
=======

Driver basics
-------------

Boatd drivers are implemented as a simple python module. When a behaviour
script requires information about the current state of the boat or needs to
send a command to some hardware, boatd runs one of the functions in the driver.

Drivers should implement functions decorated by the following:

- ``@driver.heading`` - Return the heading of the boat in degrees, relative to
  the world.

  - Returns: 0-360

- ``@driver.wind_position`` - Return the direction the wind is blowing,
  relative to the world.

  - Returns: 0-360

- ``@driver.wind_speed`` - Return the speed the wind is blowing in knots.

  - Returns: >= 0

- ``@driver.position`` - Return a tuple containing the current latitude and
  longitude of the boat, in that order.

  - Returns: (-90 - +90, -180 - +180)

- ``@driver.rudder`` - Set the boat's rudder to ``angle``  degrees relative to
  the boat.

  - Takes the arguments:

    - ``angle``: Float, -90 - +90

  - Returns: True if successful

- ``@driver.sail`` - Similarly to ``rudder``, set the sail to ``angle`` degrees
  relative to the boat.

  - Takes the arguments:

    - ``angle``: Float, -90 - +90

  - Returns: True if successful

These functions can have any name, but are marked for use and registered with
boatd using decorators.

Example, only implementing ``heading``:

.. code:: python

    import boatd
    driver = boatd.Driver()

    @driver.heading
    def get_heading():
        return some_compass.bearing()


Custom handlers
---------------

If the behaviour script needs to run some other function in the driver, a
handler can be registered using ``driver.handler(name)``

For example:

.. code:: python

    @driver.handler('pony')
    def example_handler():
        return something

This can then be used as any other function in a behaviour client.


Testing
=======

To run tests, install nose

.. code:: bash

    $ pip install nose

and run ``nosetests``. If all the tests pass, the output should be similar to:

.. code:: bash

    $ nosetests
    ..........................................
    ----------------------------------------------------------------------
    Ran 53 tests in 1.064s

    OK

The current test results from the head of the ``master`` branch can be found
`here <https://travis-ci.org/boatd/boatd>`_.

License
=======

Copyright (c) 2013-2015 Louis Taylor <louis@kragniz.eu>

Boatd is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

See [COPYING](COPYING) for more information.
