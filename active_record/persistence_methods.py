from .attribute_methods import AttributeMethods


class PersistenceMethods(AttributeMethods):
    def save(self):
        self.__class__.persistence_strategy.save(self)

    @classmethod
    def find(cls, *args, **kwargs):
        key = cls.args_as_key(*args, **kwargs)

        if not key:
            raise ValueError("Invalid key. Expected attributes: {0}".format(cls._keys))

        return cls(**cls.persistence_strategy.find(key))

    @classmethod
    def find_by(cls, **attributes):
        result_attributes = cls.persistence_strategy.find_by(attributes)
        if result_attributes:
            return cls(**result_attributes)

    @classmethod
    def args_as_key(cls, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise ValueError("Ambiguous multiple key values")

            if len(cls._keys) > 1:
                raise ValueError("Single key given but key consists of: {0}".format(cls._keys))

            return {cls._keys[0]: args[0]}

        if set(kwargs.keys()) != set(cls._keys):
            return None

        return kwargs
