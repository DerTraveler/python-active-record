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
