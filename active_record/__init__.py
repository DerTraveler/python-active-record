from .attributes import AttributeMethods
from .persistence import PersistenceMethods


class ActiveRecord(PersistenceMethods, AttributeMethods):
    """Active Record."""

    def __init__(self, *args, **kwargs):
        if type(self) == ActiveRecord:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("Can't instantiate ActiveRecord directly.")
        super().__init__(*args, **kwargs)
