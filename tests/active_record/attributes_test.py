from expects import *
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attributes, MissingAttribute, Attribute


class TestAttributes:
    def test_can_get_attributes_set_in_constructor(self):
        attrs = Attributes(name="Okarin")
        expect(attrs.get("name")).to(equal("Okarin"))

    def test_can_get_attributes_set_with_set(self):
        attrs = Attributes()
        attrs.set("name", "Okarin")
        expect(attrs.get("name")).to(equal("Okarin"))

    def test_cannot_get_unset_attributes(self):
        attrs = Attributes(name="Okarin")
        expect(lambda: attrs.get("occupation")).to(raise_error(MissingAttribute))

    def test_can_check_attribute_existence(self):
        attrs = Attributes(name="Okarin")
        expect("name" in attrs).to(be_true)
        expect("age" in attrs).to(be_false)

    def test_as_dict_returns_a_dict_of_all_attributes(self):
        attrs = Attributes(name="Okarin", age=18)
        expect(attrs.as_dict()).to(equal({"name": "Okarin", "age": 18}))


@pytest.fixture
def record():
    class TestRecord(ActiveRecord):
        id = Attribute(key=True)
        name = Attribute()

    return TestRecord


class TestAttributeMethods:
    def test_can_get_the_attributes_set_in_constructor(self, record):
        record = record(name="Okarin", age=18)
        expect(record).to(have_properties(name="Okarin", age=18))

    def test_cannot_get_unset_attributes(self, record):
        record = record(name="Okarin", age=18)
        expect(record).not_to(have_properties("occupation"))

    def test_can_set_new_attributes(self, record):
        record = record()
        record.name = "Daru"
        expect(record).to(have_properties(name="Daru"))

    def test_attributes_returns_a_dict_of_all_attributes(self, record):
        record = record(name="Suzuha")
        record.origin = 2036
        expect(record.attributes).to(equal({"name": "Suzuha", "origin": 2036}))

    def test_key_returns_key_attributes(self, record):
        record = record(id=8, name="Suzuha")
        expect(record.key).to(equal({"id": 8}))
