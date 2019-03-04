from .attributes import Attributes, Attribute


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
    def __new__(cls, name, bases, attrs):
        _attributes, keys = _extract_attributes(attrs)
        attrs["_keys"] = keys
        return super().__new__(cls, name, bases, attrs)


class AttributeMethods(metaclass=AttributesMeta):
    def __init__(self, **attributes):
        self._original_set("_attributes", Attributes(**attributes))

    @property
    def attributes(self):
        return self._attributes.as_dict()

    @property
    def key(self):
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
