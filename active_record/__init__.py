from .attributes import AttributeMethods


class ActiveRecord(AttributeMethods):
    def __init__(self, *args, **kwargs):
        if type(self) == ActiveRecord:
            raise TypeError("Can't instantiate ActiveRecord directly.")
        super().__init__(*args, **kwargs)
