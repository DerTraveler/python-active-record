from expects import *

from active_record import ActiveRecord


class TestRecord(ActiveRecord):
    pass


with describe(ActiveRecord):
    with it('cannot instantiate a ActiveRecord instance'):
        expect(ActiveRecord).to(raise_error(TypeError))

    with it('can instantiate subclasses'):
        expect(TestRecord).not_to(raise_error(TypeError))
