from expects import expect, raise_error, equal
import pytest

from active_record import ActiveRecord


class Record(ActiveRecord):
    pass


class DifferentRecord(ActiveRecord):
    pass


class ChildRecord(Record):
    pass


class TestActiveRecord:
    def test_cannot_instantiate_instance(self):
        expect(ActiveRecord).to(raise_error(TypeError))

    def test_can_instantiate_subclasses(self):
        class TestRecord(ActiveRecord):
            pass

        expect(TestRecord).not_to(raise_error(TypeError))

    class TestEqual:
        @pytest.mark.parametrize("record_a,record_b", [(Record(id=5), Record(id=5)), (Record(id=5), ChildRecord(id=5))])
        def test_are_equal(self, record_a, record_b):
            expect(record_a).to(equal(record_b))
            expect(record_b).to(equal(record_a))

        @pytest.mark.parametrize(
            "record_a,record_b",
            [
                (Record(id=5), Record(id=6)),
                (Record(id=5), Record(id=5, name="Okarin")),
                (Record(id=5), DifferentRecord(id=5)),
                (Record(id=5), ChildRecord(id=6)),
            ],
        )
        def test_are_not_equal(self, record_a, record_b):
            expect(record_a).not_to(equal(record_b))
            expect(record_b).not_to(equal(record_a))
