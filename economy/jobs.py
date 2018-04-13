from collections import namedtuple
import yaml


from . import goods


_by_name = {}
def by_name(name):
    return _by_name[name.lower()]

_jobs = []
def all():
    for job in _jobs:
        yield job


JobStep = namedtuple('JobStep', ['good','qty'])


class Job(object):
    __slots__ = ('__inputs','__outputs','__name')

    def __init__(self, name, inputs=[], outputs=[]):
        self.__name = name

        self.__inputs = ()
        for step in inputs:
            step['good'] = goods.by_name(step['good'])
            self.__inputs += (JobStep(**step),)

        self.__outputs = ()
        for step in outputs:
            step['good'] = goods.by_name(step['good'])
            self.__outputs += (JobStep(**step),)

        _by_name[name.lower()] = self
        _jobs.append(self)

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def __str__(self):
        return self.__name


with open('data/jobs.yml') as fh:
    _data = yaml.load(fh)
    for job in _data['Jobs']:
        Job(**job)

