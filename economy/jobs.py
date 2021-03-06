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
JobTool = namedtuple('JobTool', ['tool','qty','break_chance'])


class Job(object):
    __slots__ = ('__inputs','__outputs','__tools','__name','__limit')

    def __init__(self, name, inputs=[], outputs=[], tools=[], limit=None):
        self.__name = name
        self.__limit = limit

        self.__inputs = ()
        for step in inputs:
            step['good'] = goods.by_name(step['good'])
            self.__inputs += (JobStep(**step),)

        self.__outputs = ()
        for step in outputs:
            step['good'] = goods.by_name(step['good'])
            self.__outputs += (JobStep(**step),)

        self.__tools = ()
        for tool in tools:
            tool['tool'] = goods.by_name(tool['tool'])
            self.__tools += (JobTool(**tool),)

        _by_name[name.lower()] = self
        _jobs.append(self)

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    @property
    def tools(self):
        return self.__tools

    @property
    def limit(self):
        return self.__limit

    @property
    def runs(self):
        if self.limit is None:
            while True:
                yield True
        else:
            for x in range(self.limit):
                yield True

    def __str__(self):
        return self.__name


with open('data/jobs.yml') as fh:
    for job in yaml.load(fh):
        Job(**job)

