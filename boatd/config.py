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

    def __str__(self):
        return str(self.__dict__)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return default

    @classmethod
    def from_json(cls, filename):
        '''Return a Config object from a json file'''
        with open(filename) as f:
            return cls(json.load(f))

    @classmethod
    def from_yaml(cls, filename):
        '''Return a Config object from a yaml file'''
        import yaml
        with open(filename) as f:
            return cls(yaml.load(f))

    def __iter__(self):
        for d in self.__dict__:
            yield d
