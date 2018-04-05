from collections import namedtuple


_by_name = {}
def by_name(name):
    return _by_name[name.lower()]

def all():
    for good in _by_name.values():
        yield good


class Good(namedtuple('Good', ['name',])):
    __slots__ = ()
    def __init__(self, *args, **kwargs):
        _by_name[self.name.lower()] = self

    def __str__(self):
        return self.name


Sand = Good('Sand')
Glass = Good('Glass')

Ore = Good('Ore')
Metal = Good('Metal')


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

sand_digger = Recipe('SandDigger', (), ((Sand, 1),))
glass_maker = Recipe('GlassMaker', ((Sand, 2),), ((Glass, 1),))
glass_consumer = Recipe('GlassEater', ((Glass, 1),), ())

