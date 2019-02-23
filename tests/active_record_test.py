from expects import expect, raise_error

from active_record import ActiveRecord


class TestActiveRecord:
    def test_cannot_instantiate_instance(self):
        expect(ActiveRecord).to(raise_error(TypeError))

    def test_can_instantiate_subclasses(self):
        class TestRecord(ActiveRecord):
            pass

        expect(TestRecord).not_to(raise_error(TypeError))
