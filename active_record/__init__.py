from .attribute_methods import AttributeMethods
from .meta import ActiveRecordMeta
from .persistence_methods import PersistenceMethods


__all__ = ["attribute_methods", "attributes", "persistence_methods", "persistence"]


class ActiveRecord(PersistenceMethods, AttributeMethods, metaclass=ActiveRecordMeta):
    """Active Record."""

    def __init__(self, *args, **kwargs):
        if type(self) == ActiveRecord:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("Can't instantiate ActiveRecord directly.")
        super().__init__(*args, **kwargs)
