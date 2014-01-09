import json

class Config(object):
    def __init__(self, d):
        self.__dict__.update(d)
        for k, i in self.__dict__.iteritems():
            if isinstance(i, dict):
                self.__dict__[k] = Config(i)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls(json.load(f))
