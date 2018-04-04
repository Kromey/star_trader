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


RecipeStep = namedtuple('Recipe', ['good','qty_in','qty_out'])
sand_digger = (
        RecipeStep(Sand, 0, 1),
        )
glass_maker = (
        RecipeStep(Sand, 2, 0),
        RecipeStep(Glass, 0, 1),
        )
glass_consumer = (
        RecipeStep(Glass, 1, 0),
        )

