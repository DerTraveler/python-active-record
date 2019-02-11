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


class AttributeMethods():
    def __init__(self, **attributes):
        self._original_set('_attributes', Attributes(**attributes))

    @property
    def attributes(self):
        return self._attributes.as_dict()

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self._attributes.get(name)

    def __setattr__(self, name, value):
        return self._attributes.set(name, value)

    def _original_set(self, attribute, value):
        super().__setattr__(attribute, value)
