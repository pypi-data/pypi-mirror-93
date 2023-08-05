'''Main module.'''

import logging

import attr
import cattr
from ruamel.yaml import YAML

module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.INFO)


class MapperFactory:
    def __init__(self, path_format):
        self.path_format = path_format

    def patch(self, cls):
        self.cls = cls
        cls.mapper_factory = self

        self.cls.save = lambda obj: self.save(obj)
        self.cls.load = lambda **data: self.load(cls, **data)
        self.cls.filename = lambda obj: self.filename(obj)
        return self.cls

    def save(self, obj):
        data = self.data(obj)
        filename = self._filename(data)

        module_logger.debug(f'save {obj} to {filename} (from {self.path_format})')

        with open(filename, 'w') as s:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(data, s)

        return filename

    def load(self, cls, **data):
        filename = self._filename(data)

        module_logger.debug(f'load {cls} from {filename} (from {self.path_format})')

        with open(filename, 'r') as s:
            yaml = YAML()
            data_loaded = yaml.load(s)

        return self.build(cls, data_loaded)

    def build(self, cls, data):
        if hasattr(cls, 'from_dict'):
            return cls.from_dict(data)
        elif attr.has(cls):
            return cattr.structure(data, cls)
        else:
            return cls(**data)

    def data(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif attr.has(obj):
            return cattr.unstructure(obj)
        else:
            return dict(obj)

    def _filename(self, data):
        return self.path_format.format(**data)

    def filename(self, obj):
        data = self.data(obj)
        return self._filename(data)


def map_file(path_format):
    def wrapper(cls):
        m = MapperFactory(path_format)
        cls = m.patch(cls)

        return cls

    return wrapper


mapper = map_file
attrsfile = map_file


# @map_file('abc{x}.yaml')
# @attr.s()
# class D:

#     x = attr.ib(1)
#     y = attr.ib(2)

#     def to_dict(self):
#         return attr.asdict(self)

#     @classmethod
#     def from_dict(cls, d):
#         return cls(**d)
