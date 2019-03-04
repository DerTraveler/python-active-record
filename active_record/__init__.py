from .attribute_methods import AttributeMethods
from .meta import ActiveRecordMeta
from .persistence_methods import PersistenceMethods
from .query_methods import QueryMethods


__all__ = ["attribute_methods", "attributes", "persistence_methods", "persistence", "query_methods"]


class ActiveRecord(PersistenceMethods, AttributeMethods, QueryMethods, metaclass=ActiveRecordMeta):
    """Active Record."""

    def __init__(self, *args, **kwargs):
        if type(self) == ActiveRecord:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("Can't instantiate ActiveRecord directly.")
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if not (isinstance(other, type(self)) or isinstance(self, type(other))):
            return False

        return self.attributes == other.attributes
