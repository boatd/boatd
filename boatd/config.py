# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml


class Config(object):
    '''
    Allow for more natural access to the member values of a dictionary. For
    example, instead of writing:

        d = {
              'a': {
                'x': 5,
                'y': 10
              },
              'b': {
                'z': 42
              }
             }

        d['a']['x']

    we can instead write:

        c = Config(d)
        c.a.x
    '''

    def __init__(self, d):
        if d:
            self.__dict__.update(d)
            for k, i in self.__dict__.items():
                if isinstance(i, dict):
                    self.__dict__[k] = Config(i)

    def __str__(self):
        return str(self.__dict__)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return default

    @classmethod
    def from_yaml(cls, filename):
        '''Return a Config object from a yaml file'''
        with open(filename) as f:
            return cls(yaml.load(f))

    def __iter__(self):
        for d in self.__dict__:
            yield d
