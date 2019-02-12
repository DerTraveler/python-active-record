from abc import ABC, abstractmethod


class PersistenceMethods:
    def save(self):
        self.__class__.persistence_strategy.save(self)

    @classmethod
    def find(cls, single_key=None, **key):
        if single_key:
            if len(cls._keys) > 1:
                raise ValueError('Single key given but key consists of: {0}'.format(cls._keys))

            key = {cls._keys[0]: single_key}

        if set(key.keys()) != set(cls._keys):
            raise ValueError('Invalid key. Expected attributes: {0}'.format(cls._keys))

        return cls.persistence_strategy.find(key)


class PersistenceStrategy(ABC):
    @abstractmethod
    def save(self, record):
        pass

    @abstractmethod
    def find(self, key):
        pass
