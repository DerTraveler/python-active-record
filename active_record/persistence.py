"""Persistence related classes."""
from abc import ABC, abstractmethod

from .attributes import AttributeMethods


class RecordNotFound(Exception):
    """Raised when trying to access an non-existing record."""
    def __init__(self, key):
        super().__init__('Record with key {0} not found'.format(key))


class PersistenceMethods(AttributeMethods):
    """Persistence related methods."""
    def save(self):
        """Save the record."""
        self.__class__.persistence_strategy.save(self)

    @classmethod
    def find(cls, single_key=None, **key):
        """Find the record with the specified key.

        If there's only one key then passing it can be passed as single
        positional parameter. Otherwise the key attributes must be passed as
        keyword parameters.

        Raises:
            RecordNotFound: When no record with that key exists.
        """
        if single_key:
            if len(cls._keys) > 1:
                raise ValueError('Single key given but key consists of: {0}'.format(cls._keys))

            key = {cls._keys[0]: single_key}

        if set(key.keys()) != set(cls._keys):
            raise ValueError('Invalid key. Expected attributes: {0}'.format(cls._keys))

        return cls.persistence_strategy.find(key)


class PersistenceStrategy(ABC):
    """Strategy for persisting records."""
    @abstractmethod
    def save(self, record):
        """Save the specified record."""

    @abstractmethod
    def find(self, key):
        """Find the record with the specified key."""

    @staticmethod
    def raise_record_not_found(key):
        """Raises RecordNotFound exception."""
        raise RecordNotFound(key)


class InMemoryPersistence(PersistenceStrategy):
    """Persists ActiveRecords in memory."""
    def __init__(self):
        self.store = {}

    def save(self, record):
        self.store[self._hash_key(record.key)] = record

    def find(self, key):
        hashed_key = self._hash_key(key)
        if hashed_key not in self.store:
            self.raise_record_not_found(key)

        return self.store[hashed_key]

    @staticmethod
    def _hash_key(key):
        return tuple([(k, key[k]) for k in sorted(key.keys())])
