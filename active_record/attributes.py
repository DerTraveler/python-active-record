"""Attribute related classes."""
from copy import deepcopy
from collections import namedtuple


class MissingAttribute(AttributeError):
    """Raised when a nonexisting attributes is accessed."""
    def __init__(self, attribute):
        super().__init__("No attribute '{0}'".format(attribute))


class Attributes:
    """Contains Record attributes."""
    def __init__(self, **attributes):
        self._values = deepcopy(attributes)

    def set(self, attribute, value):
        """Set attribute value."""
        self._values[attribute] = value

    def get(self, attribute):
        """Get attribute value.

        Raises:
            MissingAttribute: When attribute does not exist.
        """
        if attribute not in self._values:
            raise MissingAttribute(attribute)

        return self._values[attribute]

    def as_dict(self):
        """Return the attributes as dict."""
        return deepcopy(self._values)

    def __iter__(self):
        for key in self._values:
            yield key


Attribute = namedtuple('Attribute', ['key'])


def _extract_attributes(class_attributes):
    attributes = []
    keys = []
    for name, value in class_attributes.items():
        if isinstance(value, Attribute):
            attributes.append(name)
            if value.key:
                keys.append(name)

    for attr in attributes:
        del class_attributes[attr]

    return [attributes, keys]


class AttributesMeta(type):
    """Collects key attributes specified in class definition."""
    def __new__(cls, name, bases, attrs):
        _attributes, keys = _extract_attributes(attrs)
        attrs['_keys'] = keys
        return super().__new__(cls, name, bases, attrs)


class AttributeMethods(metaclass=AttributesMeta):
    """Attribute related ActiveRecord methods."""
    def __init__(self, **attributes):
        self._original_set('_attributes', Attributes(**attributes))

    @property
    def attributes(self):
        """Returns all attributes as dict."""
        return self._attributes.as_dict()

    @property
    def key(self):
        """Returns the key of the record."""
        return {attr: self._attributes.get(attr) for attr in self._keys}

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self._attributes.get(name)

    def __setattr__(self, name, value):
        return self._attributes.set(name, value)

    def _original_set(self, attribute, value):
        super().__setattr__(attribute, value)
