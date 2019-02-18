from unittest.mock import Mock

from expects import *

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence import PersistenceStrategy, InMemoryPersistence, RecordNotFound


class TestRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)


class MultiKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)
    name = Attribute(key=True)


with describe(ActiveRecord):
    with describe('Persistence'):
        with before.each:
            TestRecord.persistence_strategy = Mock(spec=PersistenceStrategy)
            MultiKeyRecord.persistence_strategy = Mock(spec=PersistenceStrategy)

        with describe('save'):
            with it('calls save on the PersistenceStrategy'):
                record = TestRecord(name='Okabe')
                record.save()
                TestRecord.persistence_strategy.save.assert_called_with(record)

        with describe('ActiveRecord.find'):
            with context('With a single key record class'):
                with context('When giving a single key value as positional parameter'):
                    with before.each:
                        self.result = TestRecord.find(22)

                    with it('sends the right call to PersistenceStrategy'):
                        TestRecord.persistence_strategy.find.assert_called_with({'lab_member_no': 22})

                    with it('returns the return value of the strategy'):
                        expect(self.result).to(equal(TestRecord.persistence_strategy.find.return_value))

                with context('When giving the right single key value as keyword parameter'):
                    with before.each:
                        self.result = TestRecord.find(lab_member_no=22)

                    with it('sends the right call to PersistenceStrategy'):
                        TestRecord.persistence_strategy.find.assert_called_with({'lab_member_no': 22})

                    with it('returns the return value of the strategy'):
                        expect(self.result).to(equal(TestRecord.persistence_strategy.find.return_value))

                with context('When giving a wrong single key value as keyword parameter'):
                    with it('raises ValueError'):
                        expect(lambda: TestRecord.find(name='Okabe')).to(raise_error(ValueError))

                with context('When giving mutiple key values'):
                    with it('raises ValueError'):
                        expect(lambda: TestRecord.find(lab_member_no=1, name='Okabe')).to(raise_error(ValueError))

            with context('With a multiple key record class'):
                with context('When giving a single key value as positional parameter'):
                    with it('raises ValueError'):
                        expect(lambda: MultiKeyRecord.find(22)).to(raise_error(ValueError))

                with context('When giving the right key values as keyword parameter'):
                    with before.each:
                        self.result = MultiKeyRecord.find(lab_member_no=1, name='Okabe')

                    with it('sends the right call to PersistenceStrategy'):
                        MultiKeyRecord.persistence_strategy.find.assert_called_with({'lab_member_no': 1, 'name': 'Okabe'})

                    with it('returns the return value of the strategy'):
                        expect(self.result).to(equal(MultiKeyRecord.persistence_strategy.find.return_value))

                with context('When giving wrong key values as keyword parameter'):
                    with it('raises ValueError'):
                        expect(lambda: MultiKeyRecord.find(name='Okabe', age=22)).to(raise_error(ValueError))


with describe(InMemoryPersistence):
    with before.each:
        self.persistence = InMemoryPersistence()

    with shared_context('Persistence Methods'):
        with describe('save'):
            with it('can store a Record'):
                record = self.record_class(lab_member_no=1, name='Okabe')
                expect(lambda: self.persistence.save(record)).not_to(raise_error)

        with describe('find'):
            with it('can retrieve a stored Record'):
                record = self.record_class(occupation='Student', **self.record_key)
                self.persistence.save(record)
                retrieved = self.persistence.find(self.record_key)
                expect(retrieved).to(be_a(self.record_class) and have_properties(occupation='Student', **self.record_key))

            with context('when trying to retrieve a non existing Record'):
                with it('raises RecordNotFound'):
                    expect(lambda: self.persistence.find(self.record_key)).to(raise_error(RecordNotFound))

    with context('With a single key record class'):
        with before.all:
            self.record_class = TestRecord
            self.record_key = {'lab_member_no': 1}

        with included_context('Persistence Methods'):
            pass

    with context('With a multiple key record class'):
        with before.all:
            self.record_class = MultiKeyRecord
            self.record_key = {'lab_member_no': 1, 'name': 'Okabe'}

        with included_context('Persistence Methods'):
            pass
