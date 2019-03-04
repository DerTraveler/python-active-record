from unittest.mock import Mock

from expects import expect, be_a, contain_exactly
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence import PersistenceStrategy
from active_record.query_methods import QueryConditions


class Record(ActiveRecord):
    lab_member_id = Attribute(key=True)


class TestQueryMethods:
    @pytest.fixture(autouse=True)
    def reset_mocks(self):
        Record.persistence_strategy = Mock(spec=PersistenceStrategy)

    class TestAll:
        def test_returns_collection(self):
            expect(Record.all()).to(be_a(Record.Collection))

        def test_iterating_calls_query_on_strategy(self):
            Record.persistence_strategy.query.return_value = []
            list(Record.all())
            Record.persistence_strategy.query.assert_called_with(QueryConditions())

        def test_returns_queried_record(self):
            Record.persistence_strategy.query.return_value = [{"lab_member_id": 1}, {"lab_member_id": 2}]
            result = list(Record.all())
            expect(result).to(contain_exactly(Record(lab_member_id=1), Record(lab_member_id=2)))
