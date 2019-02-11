from expects import *

from active_record.attributes import Attributes, MissingAttribute


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
