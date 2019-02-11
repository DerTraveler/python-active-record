from .attributes import Attributes


class ActiveRecord:
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
