from attr import attrs, attrib
from attr.validators import instance_of


@attrs(frozen=True)
class QueryConditions:
    attributes = attrib(validator=instance_of(dict), factory=dict)

    def __and__(self, other):
        attributes = dict(self.attributes)
        attributes.update(other.attributes)
        return QueryConditions(attributes=attributes)


class QueryMethods:
    @classmethod
    def all(cls):
        return cls.Collection(QueryConditions())
