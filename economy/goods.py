from collections import namedtuple
import yaml


_by_name = {}
def by_name(name):
    return _by_name[name.lower()]

_goods = []
def all():
    for good in _goods:
        yield good


class Good(namedtuple('Good', ['name','size'])):
    __slots__ = ()
    def __init__(self, *args, **kwargs):
        _by_name[self.name.lower()] = self
        _goods.append(self)

    def __str__(self):
        return self.name


with open('data/goods.yml') as fh:
    for good in yaml.load(fh):
        Good(**good)

