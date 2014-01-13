import json


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
        self.__dict__.update(d)
        for k, i in self.__dict__.items():
            if isinstance(i, dict):
                self.__dict__[k] = Config(i)

    @classmethod
    def from_file(cls, filename):
        '''Return a Config object from a json filename'''
        with open(filename) as f:
            return cls(json.load(f))
