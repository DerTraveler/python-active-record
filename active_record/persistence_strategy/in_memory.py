from active_record.query_methods import QueryConditions
from . import PersistenceStrategy


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
        records_with_attributes = self.query(QueryConditions(attributes=attributes))
        return next(records_with_attributes, None)

    def query(self, conditions):
        for record in self.store.values():
            if self._dict_contains(record, conditions.attributes):
                yield record

    def key_exists(self, key, conditions):
        return self.exists(conditions & QueryConditions(attributes=key))

    def exists(self, conditions):
        try:
            records = self.query(conditions)
            next(records)
            return True
        except StopIteration:
            return False

    @staticmethod
    def _hash_key(key):
        return tuple([(k, key[k]) for k in sorted(key.keys())])

    @staticmethod
    def _dict_contains(dict_a, dict_b):
        for k, v in dict_b.items():
            if k not in dict_a or dict_a[k] != v:
                return False
        return True
