from collections import namedtuple


_by_name = {}
def by_name(name):
    return _by_name[name.lower()]


class Commodity(namedtuple('Commodity', ['name',])):
    __slots__ = ()
    def __init__(self, *args, **kwargs):
        _by_name[self.name.lower()] = self

    def __str__(self):
        return self.name


Sand = Commodity('Sand')
Glass = Commodity('Glass')

Ore = Commodity('Ore')
Metal = Commodity('Metal')


RecipeStep = namedtuple('Recipe', ['commodity','qty_in','qty_out'])
glass_recipe = (
        RecipeStep(Sand, 2, 0),
        RecipeStep(Glass, 0, 1),
        )

