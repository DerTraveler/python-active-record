from unittest.mock import Mock

from expects import expect, equal
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence_strategy import PersistenceStrategy
from active_record.query_methods import QueryConditions


class Record(ActiveRecord):
    lab_member_no = Attribute(key=True)


class TwoKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)
    name = Attribute(key=True)


class TestCollection:
    @pytest.fixture(autouse=True)
    def reset_mocks(self):
        Record.persistence_strategy = Mock(spec=PersistenceStrategy)
        TwoKeyRecord.persistence_strategy = Mock(spec=PersistenceStrategy)

    class TestExists:
        @pytest.mark.parametrize("strategy_result", [True, False])
        @pytest.mark.parametrize(
            "record_class,exist_args,exist_kwargs,expected_key",
            [
                (Record, [1], {}, {"lab_member_no": 1}),
                (Record, [], {"lab_member_no": 2}, {"lab_member_no": 2}),
                (TwoKeyRecord, [], {"lab_member_no": 1, "name": "Okarin"}, {"lab_member_no": 1, "name": "Okarin"}),
            ],
        )
        def test_with_key(self, record_class, exist_args, exist_kwargs, expected_key, strategy_result):
            record_class.persistence_strategy.key_exists.return_value = strategy_result
            conditions = QueryConditions()
            collection = record_class.Collection(conditions)

            result = collection.exists(*exist_args, **exist_kwargs)

            record_class.persistence_strategy.key_exists.assert_called_with(expected_key, conditions)
            expect(result).to(equal(strategy_result))

        @pytest.mark.parametrize("strategy_result", [True, False])
        @pytest.mark.parametrize("record_class", [Record, TwoKeyRecord])
        def test_with_attributes(self, record_class, strategy_result):
            record_class.persistence_strategy.exists.return_value = strategy_result
            conditions = QueryConditions(attributes={"age": 17})
            collection = record_class.Collection(conditions)

            result = collection.exists(occupation="Student")

            record_class.persistence_strategy.exists.assert_called_with(
                QueryConditions(attributes={"age": 17, "occupation": "Student"})
            )
            expect(result).to(equal(strategy_result))
