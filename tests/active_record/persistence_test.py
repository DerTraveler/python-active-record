from unittest.mock import Mock

from expects import *
import pytest

from active_record import ActiveRecord
from active_record.attributes import Attribute
from active_record.persistence import PersistenceStrategy, InMemoryPersistence, RecordNotFound


class SingleKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)


class MultiKeyRecord(ActiveRecord):
    lab_member_no = Attribute(key=True)
    name = Attribute(key=True)


@pytest.fixture(autouse=True)
def reset_mocks():
    SingleKeyRecord.persistence_strategy = Mock(spec=PersistenceStrategy)
    MultiKeyRecord.persistence_strategy = Mock(spec=PersistenceStrategy)


def single_key_record():
    return SingleKeyRecord(lab_member_no=1)


def multi_key_record():
    return MultiKeyRecord(lab_member_no=1, name='Okarin')


class TestPersistence:
    @pytest.mark.parametrize('record', [
        single_key_record(),
        multi_key_record()
    ])
    def test_save_calls_save_on_strategy(self, record):
        record.save()
        record.persistence_strategy.save.assert_called_with(record)

    @pytest.mark.parametrize('record_class,find_args,expected_args', [
        (SingleKeyRecord, ([1], {}), {'lab_member_no': 1}),
        (SingleKeyRecord, ([], {'lab_member_no': 1}), {'lab_member_no': 1}),
        (MultiKeyRecord, ([], {'lab_member_no': 1, 'name': 'Okarin'}), {'lab_member_no': 1, 'name': 'Okarin'})
    ])
    def test_find_success(self, record_class, find_args, expected_args):
        args, kwargs = find_args
        result = record_class.find(*args, **kwargs)
        record_class.persistence_strategy.find.assert_called_with(expected_args)
        expect(result).to(equal(record_class.persistence_strategy.find.return_value))

    @pytest.mark.parametrize('record_class,find_args', [
        (SingleKeyRecord, ([], {'name': 'Okarin'})),
        (SingleKeyRecord, ([], {'lab_member_no': 1, 'name': 'Okarin'})),
        (MultiKeyRecord, ([1], {})),
        (MultiKeyRecord, ([], {'occupation': 'Student', 'name': 'Okarin'})),
    ])
    def test_find_failure(self, record_class, find_args):
        args, kwargs = find_args
        expect(lambda: record_class.find(*args, **kwargs)).to(raise_error(ValueError))


class TestInMemoryPersistence:
    @pytest.fixture
    def strategy(self):
        return InMemoryPersistence()

    @pytest.mark.parametrize('record', [
        single_key_record(),
        multi_key_record()
    ])
    def test_save(self, record, strategy):
        expect(lambda: strategy.save(record)).not_to(raise_error)

    @pytest.mark.parametrize('record', [
        single_key_record(),
        multi_key_record()
    ])
    def test_find_success(self, record, strategy):
        strategy.save(record)
        retrieved = strategy.find(record.key)
        expect(retrieved).to(equal(record))

    def test_find_nonexisting(self, strategy):
        expect(lambda: strategy.find({'key': 'nonexisting'})).to(raise_error(RecordNotFound))
