from expects import *

from active_record.attributes import Attributes


with describe(Attributes):
    with it('can get attributes set in the constructor'):
        attrs = Attributes(name='Okarin')
        expect(attrs.get('name')).to(equal('Okarin'))

    with it('can get attributes set with the set method'):
        attrs = Attributes()
        attrs.set('name', 'Okarin')
        expect(attrs.get('name')).to(equal('Okarin'))
