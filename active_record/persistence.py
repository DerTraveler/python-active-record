from abc import ABC, abstractmethod


class RecordNotFound(Exception):
    def __init__(self, key):
        super().__init__('Record with key {0} not found'.format(key))


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

    def raise_record_not_found(self, key):
        raise RecordNotFound(key)


class InMemoryPersistence(PersistenceStrategy):
    def __init__(self):
        self.store = {}

    def save(self, record):
        self.store[self._hash_dict(record.key)] = record

    def find(self, key):
        hashed_key = self._hash_dict(key)
        if hashed_key not in self.store:
            self.raise_record_not_found(key)

        return self.store[hashed_key]

    @staticmethod
    def _hash_dict(d):
        return tuple([(k, d[k]) for k in sorted(d.keys())])
