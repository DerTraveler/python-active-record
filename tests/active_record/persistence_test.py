from expects import expect, equal, raise_error
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence import InMemoryPersistence, RecordNotFound


class SingleKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)

    @classmethod
    def instance(cls):
        return cls(lab_member_no=1, occupation="Student")


class MultiKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)
    name = Attribute(key=True)

    @classmethod
    def instance(cls):
        return cls(lab_member_no=1, name="Okarin", occupation="Student")


class TestInMemoryPersistence:
    @pytest.fixture
    def strategy(self):
        return InMemoryPersistence()

    @pytest.mark.parametrize("record", [SingleKeyRecord.instance(), MultiKeyRecord.instance()])
    def test_save(self, record, strategy):
        expect(lambda: strategy.save(record)).not_to(raise_error)

    class TestFind:
        @pytest.mark.parametrize("record", [SingleKeyRecord.instance(), MultiKeyRecord.instance()])
        def test_success(self, record, strategy):
            strategy.save(record)
            retrieved = strategy.find(record.key)
            expect(retrieved).to(equal(record))

        def test_nonexisting(self, strategy):
            expect(lambda: strategy.find({"key": "nonexisting"})).to(raise_error(RecordNotFound))

    class TestFindBy:
        @pytest.mark.parametrize("record", [SingleKeyRecord.instance(), MultiKeyRecord.instance()])
        def test_success(self, record, strategy):
            strategy.save(record)
            retrieved = strategy.find_by({"occupation": "Student"})
            expect(retrieved).to(equal(record))

        def test_nonexisting(self, strategy):
            expect(lambda: strategy.find_by({"attribute": "nonexisting"})).to(raise_error(RecordNotFound))
