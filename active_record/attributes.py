from copy import deepcopy


class MissingAttribute(AttributeError):
    def __init__(self, attribute):
        super().__init__("No attribute '{0}'".format(attribute))


class Attributes:
    def __init__(self, **attributes):
        self._values = deepcopy(attributes)

    def set(self, attribute, value):
        self._values[attribute] = value

    def get(self, attribute):
        if attribute not in self._values:
            raise MissingAttribute(attribute)

        return self._values[attribute]

    def as_dict(self):
        return deepcopy(self._values)

    def __iter__(self):
        for key in self._values:
            yield key
