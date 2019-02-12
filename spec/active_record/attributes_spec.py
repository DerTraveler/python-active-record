from expects import *

from active_record import ActiveRecord
from active_record.attributes import Attributes, MissingAttribute, Attribute


with describe(Attributes):
    with it('can get attributes set in the constructor'):
        attrs = Attributes(name='Okarin')
        expect(attrs.get('name')).to(equal('Okarin'))

    with it('can get attributes set with the set method'):
        attrs = Attributes()
        attrs.set('name', 'Okarin')
        expect(attrs.get('name')).to(equal('Okarin'))

    with it('cannot get attributes unset attributess'):
        attrs = Attributes(name='Okarin')
        expect(lambda: attrs.get('occupation')).to(raise_error(MissingAttribute))

    with it('can check for attribute existence'):
        attrs = Attributes(name='Okarin')
        expect('name' in attrs).to(be_true)
        expect('age' in attrs).to(be_false)

    with describe('as_dict'):
        with it('returns a dict of all the attributes'):
            attrs = Attributes(name='Okarin', age=18)
            expect(attrs.as_dict()).to(equal({'name': 'Okarin', 'age': 18}))


class TestRecord(ActiveRecord):
    id = Attribute(key=True)


with describe(ActiveRecord):
    with describe('Attribute methods'):
        with it('can get the attributes set in the constructor'):
            record = TestRecord(name='Okarin', age=18)
            expect(record).to(have_properties(name='Okarin', age=18))

        with it('cannot get unset attributes'):
            record = TestRecord(name='Okarin', age=18)
            expect(record).not_to(have_properties('occupation'))

        with it('can set new attributes'):
            record = TestRecord()
            record.name = 'Daru'
            expect(record).to(have_properties(name='Daru'))

        with describe('attributes'):
            with it('returns a dict of all set attributes'):
                record = TestRecord(name='Suzuha')
                record.origin = 2036
                expect(record.attributes).to(equal({'name': 'Suzuha', 'origin': 2036}))

        with describe('key'):
            with it('returns the key attributes'):
                record = TestRecord(id=8, name='Suzuha')
                expect(record.key).to(equal({'id': 8}))
