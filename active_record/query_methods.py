from attr import attrs, attrib
from attr.validators import instance_of

from .collection import build_collection_class


class QueryMethodsMeta(type):
    def __new__(cls, name, bases, attrs):
        record_class = super().__new__(cls, name, bases, attrs)
        record_class.Collection = build_collection_class(record_class)
        return record_class


@attrs(frozen=True)
class QueryConditions:
    attributes = attrib(validator=instance_of(dict), factory=dict)


class QueryMethods:
    @classmethod
    def all(cls):
        return cls.Collection(QueryConditions())
