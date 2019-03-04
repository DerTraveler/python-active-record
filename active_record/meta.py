from .attribute_methods import AttributesMethodsMeta
from .query_methods import QueryMethodsMeta


class ActiveRecordMeta(AttributesMethodsMeta, QueryMethodsMeta):
    pass
