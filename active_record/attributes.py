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


class Attribute:
    def __init__(self, key=False):
        self.key = key


def _extract_attributes(class_attributes):
    attributes = []
    keys = []
    for name, value in class_attributes.items():
        if isinstance(value, Attribute):
            attributes.append(name)
            if value.key:
                keys.append(name)

    for a in attributes:
            del class_attributes[a]

    return [attributes, keys]


class AttributesMeta(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        _attributes, keys = _extract_attributes(attrs)
        attrs['_keys'] = keys
        return super().__new__(mcs, name, bases, attrs)


class AttributeMethods(metaclass=AttributesMeta):
    def __init__(self, **attributes):
        self._original_set('_attributes', Attributes(**attributes))

    @property
    def attributes(self):
        return self._attributes.as_dict()

    @property
    def key(self):
        return {attr: self._attributes.get(attr) for attr in self.__class__._keys}

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self._attributes.get(name)

    def __setattr__(self, name, value):
        return self._attributes.set(name, value)

    def _original_set(self, attribute, value):
        super().__setattr__(attribute, value)
