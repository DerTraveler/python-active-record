from .query_methods import QueryConditions


class ActiveRecordCollection:
    class Iterator:
        def __init__(self, record_class, *, conditions):
            self.record_class = record_class
            self.conditions = conditions

        def get_elements(self):
            for attributes in self.record_class.persistence_strategy.query(self.conditions):
                yield self.record_class(**attributes)

    def __init__(self, conditions):
        self.conditions = conditions

    def __iter__(self):
        iterator = self.Iterator(self.Record, conditions=self.conditions)
        return iterator.get_elements()

    def exists(self, *args, **attributes):
        key = self.Record.args_as_key(*args, **attributes)
        if key:
            return self.Record.persistence_strategy.key_exists(key, self.conditions)

        return self.Record.persistence_strategy.exists(self.conditions and QueryConditions(attributes=attributes))
