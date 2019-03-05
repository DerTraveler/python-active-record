from .attribute_methods import AttributesMethodsMeta
from .collection import ActiveRecordCollection


def _build_collection_class(record_class):
    return type("{0}Collection".format(record_class.__name__), (ActiveRecordCollection,), {"Record": record_class})


class QueryMethodsMeta(type):
    def __new__(cls, name, bases, attrs):
        record_class = super().__new__(cls, name, bases, attrs)
        record_class.Collection = _build_collection_class(record_class)
        return record_class


class ActiveRecordMeta(AttributesMethodsMeta, QueryMethodsMeta):
    pass
