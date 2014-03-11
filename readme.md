boatd - sailing boat daemon [![BuildStatus](https://travis-ci.org/boatd/boatd.png?branch=master)](https://travis-ci.org/boatd/boatd)
===========================

Experimental robotic sailing boat daemon.

General architecture
-----------

Boatd is designed to be the manager for a boat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using `boatd`:

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

### Locally with virtualenv

Install virtualenv and pip

    $ sudo easy_install virtualenv pip

Now setup the virtual environment and install the dependencies

    $ mkdir env
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

### System-wide on Debian

On any Debian based distribution:

    $ apt-get install python-yaml


Testing
-------

To run tests, install nose

    $ pip install nose

and run `nosetests`. If all the tests pass, the output should be similar to:

    $ nosetests 
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.118s

    OK


Todo
----

  - ~~Behaviour loading~~
  - Driver loading
  - Core boatd function decorators
  - Logging
  - Event system
  - API
  - Halisim driver
  - Other language support
  - init system integration
  - Remote behaviour loading
