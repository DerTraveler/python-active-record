from expects import expect, equal, raise_error, be_none, contain_only
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence import InMemoryPersistence, RecordNotFound
from active_record.query_methods import QueryConditions


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
            expect(retrieved).to(equal(record.attributes))

        def test_nonexisting(self, strategy):
            expect(lambda: strategy.find({"key": "nonexisting"})).to(raise_error(RecordNotFound))

    class TestFindBy:
        @pytest.mark.parametrize("record", [SingleKeyRecord.instance(), MultiKeyRecord.instance()])
        def test_success(self, record, strategy):
            strategy.save(record)
            retrieved = strategy.find_by({"occupation": "Student"})
            expect(retrieved).to(equal(record.attributes))

        def test_nonexisting(self, strategy):
            expect(strategy.find_by({"attribute": "nonexisting"})).to(be_none)

    class TestQuery:
        @pytest.mark.parametrize(
            "records",
            [
                [SingleKeyRecord(lab_member_no=1, occupation="Student"), SingleKeyRecord(lab_member_no=2, occupation="Superhacker")],
                [
                    MultiKeyRecord(lab_member_no=1, name="Okarin", occupation="Student"),
                    SingleKeyRecord(lab_member_no=2, name="Daru", occupation="Superhacker"),
                ],
            ],
        )
        def test_without_conditions(self, records, strategy):
            for r in records:
                strategy.save(r)
            retrieved = strategy.query(QueryConditions())
            expect(retrieved).to(contain_only(*[r.attributes for r in records]))

        def test_with_attribute_conditions(self, strategy):
            records = [
                {"lab_member_no": 1, "occupation": "Student"},
                {"lab_member_no": 2, "occupation": "Student"},
                {"lab_member_no": 3, "occupation": "Cosplayer"},
            ]
            for r in records:
                strategy.save(SingleKeyRecord(**r))
            retrieved = strategy.query(QueryConditions(attributes={"occupation": "Student"}))
            expect(retrieved).to(contain_only(records[0], records[1]))
