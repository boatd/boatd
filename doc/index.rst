===================
boatd documentation
===================

.. contents::
   :backlinks: none

Introduction
============

Boatd is designed to be the manager for a boat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using boatd:

- the *driver* interfaces with the particular set of hardware in the boat.

- the *behaviour* performs a set of actions to make the boat do a
  particular task. The API available for these scripts is supposed to be
  declarative, with the idea that for any boat with a driver written, any
  behaviour script will work.

.. figure:: _static/boatd-arch.png
   :scale: 50 %


Installing
==========

Boatd is currently tested and supported on Python 2.7 and 3.4. Support for
python 2 may be dropped in the near future.

Installing in a virtualenv from PyPi (recommended)
--------------------------------------------------

This installs boatd in a `virtualenv
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_, keeping it separate from the rest of the system.
First, create a new virtualenv::

    $ virtualenv env

Activate this virtualenv::

    $ source env/bin/activate

Install boatd and its dependencies from the latest published stable release::

    $ pip install boatd


Installing with Docker
----------------------

    $ docker build -t boatd .


Installing for development
--------------------------

First, clone the repository and change to the directory::

    $ git clone https://github.com/boatd/boatd.git
    $ cd boatd

Create a new virtualenv::

    $ virtualenv boatd-dev-env

Activate this virtualenv::

    $ source boatd-dev-env/bin/activate

Install boatd in editable mode from the local copy::

    $ pip install --editable .

Installing when you don't care and live life on the edge (system wide installation)
-----------------------------------------------------------------------------------

First install dependencies:

On any Debian based distribution (Debian, Ubuntu, Mint etc):

.. code:: bash

    $ apt-get install python-yaml

On Red Hat systems (Fedora, CentOS, etc):

.. code:: bash

    $ dnf install PyYAML

Then clone the repository and change to the directory::

    $ git clone https://github.com/boatd/boatd.git
    $ cd boatd

Run the installer::

    $ sudo python setup.py install

Running boatd
=============

Running with Docker:
--------------------

Assumming you have built the docker image locally:

Quick-start:

.. code:: bash

    $ docker run -d -p 2222:2222 boatd
    $ curl localhost:2222
    {"boatd": {"version": 1.3}}

By default, the image uses the example configuration, drivers and behaviours. 

There are three major ways to develop using this Docker image. 

1. Modify the configuration and mount the custom configuration.
2. Simply mount a directory (e.g. for plugins, drivers or behaviours).
3. A combination of the above.

For example, to use a custom driver:

.. code:: bash
    # Create some directories to hold our new work
    $ mkdir config && mkdir drivers

    # Update default config to use "my_awesome_driver.py"
    $ sed 's/basic_driver\.py/my_awesome_driver\.py/' boatd-config.yaml.example > config/custom-boatd-config.yaml

    # Make a modified copy of the "basic_driver.py"
    $ sed 's/MyFancy/MyAwesome/' example/basic_driver.py > drivers/my_awesome_driver.py

    # Run with MyAwesomeBoatDriver
    $ docker run -v `pwd`:/opt/boatd -e CONFIG=/opt/boatd/config/custom-boatd-config.yaml -p 2222:2222 boatd


Running locally:
--------

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

	driver:
		file: example/basic_driver.py

	behaviours:
		- example:
			file: example/basic_behaviour.py


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


``/wind``
---------

- ``GET``

  Returns properties of the wind. Example output:

  .. code:: json

    {
      "direction": 8.42,
      "speed": 25
    }


``/waypoints``
--------------

- ``GET``

  Returns the active set of waypoints

  .. code:: json

    {
      "current": [1.0, 1.0],
      "home": [0.0, 0.0],
      "waypoints": [
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0]
      ]
    }


- ``POST``

  Add to the current set of waypoints

  .. code:: json

    {
      "waypoints": [
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0]
      ]
    }


``/behaviours``
---------------

- ``GET``

  Returns data about available and current behaviours. Example output:

  .. code:: json

    {
      "current": null,
      "behaviours": {
        "basic": {
          "filename": "example/basic_behaviour.py",
          "running": false
        }
      }
    }

- ``POST``

  Change the currently running behaviour. Setting the current behaviour to
  ``null`` will cause no behaviour to be run.

  Examples:

  .. code:: json

       {
         "current": null
       }


  .. code:: json

       {
         "current": "basic"
       }


Drivers
=======

Driver basics
-------------

Boatd drivers are implemented as a simple user defined class in a loadable
python module.  When a behaviour script requires information about the current
state of the boat or needs to send a command to some hardware, boatd runs one
of the methods in the driver.

To write a driver, a python module should be created that contains an object
named ``driver``. This object must be an instance of a class inheriting from
and implementing the interface defined in ``BaseBoatdDriver``:

.. autoclass:: boatd.BaseBoatdDriver
   :members:

Note that the driver instance **must** be named ``driver``, otherwise boatd
won't know where to find it.

Example driver
--------------

An example:

.. code:: python

    import boatd

    class MyFancyBoatDriver(boatd.BaseBoatdDriver):
        def __init__(self):
            # initialize some things here
            pass

        def heading(self):
            return 30.0

        def wind_direction(self):
            return 45.0

        def wind_speed(self):
            return 4.0

        def position(self):
            return (0, 0)

        def rudder(self, angle):
            print('moving rudder to', angle)

        def sail(self, angle):
            print('moving sail to', angle)

        def reconnect(self):
                pass
    # create an instance of the driver class
    driver = MyFancyBoatDriver()


Configuring boatd to use a driver
---------------------------------

Once you've written a driver, you can tell boatd to load it as the active
driver by setting ``scripts.driver`` in your configuration file. Eg:

.. code:: yaml

    scripts:
        driver: example/driver.py

This can be a relative path, as with the example above. It can also be
absolute. boatd will also expand ``~`` to your home directory:

.. code:: yaml

    scripts:
        driver: ~/git/sails-boatd-driver/driver.py


Plugins
=======

Plugins are loadable python modules that run in a separate thread inside boatd.
They have access to the current data about the boat.

Plugins are enabled with the main boatd configuration file. Each plugin may
have a few extra parameters, but all have the ``enabled`` parameter to enable
or disable it.

Example:

.. code-block:: yaml

    plugins:
      - some_plugin_name:
        enabled: true


Bundled plugins
---------------

Boatd comes with a few plugins preinstalled. These are:

- ``logger``

  This logs data about the current state of the boat to a file periodically.

  Configuration parameters:

    - ``period`` - the time in seconds between each logged line

    - ``filename`` - the path to the file logs will be written to

    Example:

    .. code-block:: yaml

        plugins:
          - logger:
            enabled: true
            period: 10
            filename: logs/log_trace

- ``gpx_logger``

  This logs data about the current state of the boat to a GPX formatted file periodically.

  Configuration parameters:

    - ``period`` - the time in seconds between each logged line

    - ``filename`` - the path to the file logs will be written to, the filename
    will be appended with a timestamp

    Example:

    .. code-block:: yaml

        plugins:
          - gpx_logger:
            enabled: true
            period: 1
            filename: logs/gpx_log

- ``mavlink``

  This allows boatd to communicate using a subset of the mavlink protocol.

  Configuration parameters:

    - ``device`` - the serial port to use

    - ``baud`` - baud rate to use with the serial port

  Example:

  .. code-block:: yaml

      plugins:
        - mavlink:
          enabled: true
          device: /dev/ttyUSB0
          baud: 115200


Writing new plugins
-------------------

To implement a plugin, a class must be implemented that conforms to a certain
interface (similar to how drivers are defined). The interface is simple:

.. autoclass:: boatd.BasePlugin
   :members:

An example implementation would be:

.. code:: python

    from boatd import BasePlugin

    class ExamplePlugin(BasePlugin):
        def main(self):
            while self.running:
                position = self.boatd.boat.position()
                print('logging some stuff ', position)

    plugin = LoggerPlugin


Some things to note:

- You automatically get access to an object called ``self.boatd``. This
  contains a ``boat`` attribute which you can use to interact with the live
  boat.
- ``self.running`` can be used to check if the plugin should end. When the
  plugin is started by boatd, this will be set to ``True``. When boatd is about
  to quit or plugins need to be stopped for some other reason, it will be set
  to ``False``.


python-boatdclient
==================

Boatd has a client library written for python. It contains a python wrapper
module and a command line client.

You can install python-boatdclient from PyPi by running::

    $ pip install python-boatdclient

Boatdclient includes the following user facing classes:

.. autoclass:: boatdclient.Boat
   :members:

.. autoclass:: boatdclient.Behaviour
   :members:

``Boat`` returns and uses special classes for bearings and latitude longitude
points. These contain some common functionality.

.. autoclass:: boatdclient.Point
   :members:

.. autoclass:: boatdclient.Bearing
   :members:


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
