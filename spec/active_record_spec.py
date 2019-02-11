from expects import *

from active_record import ActiveRecord


class TestRecord(ActiveRecord):
    pass


with describe(ActiveRecord):
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