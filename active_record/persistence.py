from abc import ABC, abstractmethod


class RecordNotFound(Exception):
    def __init__(self, key):
        super().__init__("Record with key {0} not found".format(key))


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

    @abstractmethod
    def query(self, conditions):
        pass

    @abstractmethod
    def key_exists(self, key, conditions):
        pass

    @abstractmethod
    def exists(self, conditions):
        pass

    @staticmethod
    def raise_record_not_found(key):
        raise RecordNotFound(key)


class InMemoryPersistence(PersistenceStrategy):
    def __init__(self):
        self.store = {}

    def save(self, record):
        self.store[self._hash_key(record.key)] = record.attributes

    def find(self, key):
        hashed_key = self._hash_key(key)
        if hashed_key not in self.store:
            self.raise_record_not_found(key)

        return self.store[hashed_key]

    def find_by(self, attributes):
        for record in self.store.values():
            if self._dict_contains(record, attributes):
                return record

    def query(self, conditions):
        for record in self.store.values():
            if self._dict_contains(record, conditions.attributes):
                yield record

    def key_exists(self, key, conditions):
        pass

    def exists(self, conditions):
        pass

    @staticmethod
    def _hash_key(key):
        return tuple([(k, key[k]) for k in sorted(key.keys())])

    @staticmethod
    def _dict_contains(dict_a, dict_b):
        for k, v in dict_b.items():
            if k not in dict_a or dict_a[k] != v:
                return False
        return True
