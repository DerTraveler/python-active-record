from abc import ABC, abstractmethod

from .attribute_methods import AttributeMethods


class RecordNotFound(Exception):
    def __init__(self, key):
        super().__init__("Record with key {0} not found".format(key))


class PersistenceMethods(AttributeMethods):
    def save(self):
        self.__class__.persistence_strategy.save(self)

    @classmethod
    def find(cls, single_key=None, **key):
        if single_key:
            if len(cls._keys) > 1:
                raise ValueError("Single key given but key consists of: {0}".format(cls._keys))

            key = {cls._keys[0]: single_key}

        if set(key.keys()) != set(cls._keys):
            raise ValueError("Invalid key. Expected attributes: {0}".format(cls._keys))

        return cls.persistence_strategy.find(key)

    @classmethod
    def find_by(cls, **attributes):
        return cls.persistence_strategy.find_by(attributes)


class PersistenceStrategy(ABC):
    @abstractmethod
    def save(self, record):
        pass

    @abstractmethod
    def find(self, key):
        pass

    @abstractmethod
    def find_by(self, attributes):
        pass

    @staticmethod
    def raise_record_not_found(key):
        raise RecordNotFound(key)


class InMemoryPersistence(PersistenceStrategy):
    def __init__(self):
        self.store = {}

    def save(self, record):
        self.store[self._hash_key(record.key)] = record

    def find(self, key):
        hashed_key = self._hash_key(key)
        if hashed_key not in self.store:
            self.raise_record_not_found(key)

        return self.store[hashed_key]

    def find_by(self, attributes):
        for record in self.store.values():
            if self._record_has_attributes(record, attributes):
                return record

        self.raise_record_not_found({})

    @staticmethod
    def _hash_key(key):
        return tuple([(k, key[k]) for k in sorted(key.keys())])

    @staticmethod
    def _record_has_attributes(record, attributes):
        try:
            for k, v in attributes.items():
                if getattr(record, k) != v:
                    return False
            return True
        except AttributeError:
            return False
