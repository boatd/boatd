boatd - sailing boat daemon
===========================

Experimental robotic sailing boat daemon.

Terminology
-----------

  - `Behaviour` - performs a set of actions to make the boat do a particular task
  - `Driver` - causes hardware to do interesting things based on actions

```
           boatd
             |
        -----------
       |           |
     driver     behaviour
       |
  boat hardware
```

Dependencies
------------

    $ sudo apt-get install python-yaml


Todo
----

  - Behaviour loading
  - Driver loading
  - Core boatd function decorators
  - Logging
  - Event system
  - API
  - Halisim driver
  - Other language support
  - init system integration
  - Remote behaviour loading
