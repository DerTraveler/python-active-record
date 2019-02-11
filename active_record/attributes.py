from copy import deepcopy


class Attributes:
    def __init__(self, **attributes):
        self._values = deepcopy(attributes)

    def set(self, attribute, value):
        self._values[attribute] = value

    def get(self, attribute):
        return self._values[attribute]
