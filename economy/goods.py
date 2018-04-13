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
    _data = yaml.load(fh)
    for good in _data['Goods']:
        Good(**good)


RecipeStep = namedtuple('RecipeStep', ['good','qty'])


class Recipe(object):
    __slots__ = ('__inputs','__outputs','__name')

    def __init__(self, name, inputs, outputs):
        self.__name = name

        self.__inputs = ()
        for step in inputs:
            self.__inputs += (RecipeStep(*step),)

        self.__outputs = ()
        for step in outputs:
            self.__outputs += (RecipeStep(*step),)

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def __str__(self):
        return self.__name

sand_digger = Recipe('SandDigger', (), ((by_name('Sand'), 1),))
glass_maker = Recipe('GlassMaker', ((by_name('Sand'), 2),), ((by_name('Glass'), 1),))
glass_consumer = Recipe('GlassEater', ((by_name('Glass'), 1),), ())

