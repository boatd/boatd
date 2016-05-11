===================
boatd documentation
===================

Contents:

.. contents::

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

    $ dnf install PyYAML
    $ python setup.py install


Running boatd
=============

.. code:: bash

    $ boatd --help
    usage: boatd [-h] [--version] [CONFIG FILE]

    Experimental robotic sailing boat daemon.

    positional arguments:
      CONFIG FILE  a path to a configuration file

    optional arguments:
      -h, --help   show this help message and exit
      --version    show program's version number and exit


After you have installed boatd, it can be run with ``$ boatd``.

You will need to create a configuration file. It should look something like:

.. code:: yaml

    boatd:
      port: 2222
      interface: 127.0.0.1

    plugin_directory: null

    plugins:
      - logger:
        period: 10
        filename: logs/gps_trace

    scripts:
      behaviour: example/basic_behaviour.py
      driver: example/basic_driver.py

The example config file (``boatd-config.yaml.example``) can be modified for
your boat.

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

- ``@driver.wind_direction`` - Return the direction the wind is blowing,
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

To run tests, install tox

.. code:: bash

    $ pip install tox

and run ``tox``. If all the tests pass, the output should be similar to:

.. code::

    $ tox
    GLOB sdist-make: /home/louis/git/boatd/setup.py
    py27 inst-nodeps: /home/louis/git/boatd/.tox/dist/boatd-1.1.3.zip
    py27 installed: boatd==1.1.3,coverage==4.0.2,coveralls==1.1,docopt==0.6.2,p
    luggy==0.3.1,py==1.4.30,pytest==2.8.2,pytest-cov==2.2.0,PyYAML==3.11,reques
    ts==2.8.1,tox==2.2.1,virtualenv==13.1.2,wheel==0.24.0
    py27 runtests: PYTHONHASHSEED='2985615961'
    py27 runtests: commands[0] | py.test -v --cov boatd boatd
    ========================= test session starts ==========================
    platform linux2 -- Python 2.7.10, pytest-2.8.2, py-1.4.30, pluggy-0.3.1 --
    /home/louis/git/boatd/.tox/py27/bin/python2.7
    cachedir: .cache
    rootdir: /home/louis/git/boatd, inifile: 
    plugins: cov-2.2.0
    collected 50 items 

    boatd/tests/test_api.py::TestAPI::test_GET PASSED
    boatd/tests/test_api.py::TestAPI::test_content_type PASSED

    ... snipped

    ====================== 50 passed in 1.39 seconds =======================
    _______________________________ summary ________________________________
      py27: commands succeeded
      py34: commands succeeded
      pypy: commands succeeded
      flake8: commands succeeded
      congratulations :)

This will run all test environments. To run an individual environment, run
``tox -e py27``, or more generally ``tox -e <env>``, replacing env with
``py27``, ``py34``, ``pypy`` or ``flake8`` (style checks).

The current test results from the head of the ``master`` branch can be found
`here <https://travis-ci.org/boatd/boatd>`_.


Indices and tables
==================

* :ref:`genindex`
