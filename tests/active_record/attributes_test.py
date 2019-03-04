from expects import expect, equal, raise_error, be_true, be_false

from active_record.attributes import Attributes, MissingAttribute


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
