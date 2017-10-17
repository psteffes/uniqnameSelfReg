from django.test import SimpleTestCase
from ..serializers import TokenSerializer, SuggestionSerializer, UniqnameSerializer, PasswordSerializer


class TokenSerializerTests(SimpleTestCase):

    def test_valid_data(self):
        umid = '00123400'    # no zero trimming
        data = {'umid': umid}
        serializer = TokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['umid'], umid)

    def test_invalid_data(self):
        data = {'umid': 'abc123'}
        serializer = TokenSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['umid'], ['Enter a valid UMID.'])

    def test_required_fields(self):
        serializer = TokenSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['umid'], ['This field is required.'])


class SuggestionSerializerTests(SimpleTestCase):

    def test_valid_data(self):
        dn = 'my_dn'
        name_parts = ['mega', 'man']
        data = {
            'dn': dn,
            'name_parts': name_parts,
        }
        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['dn'], dn)
        self.assertEqual(serializer.validated_data['name_parts'], name_parts)

    def test_invalid_data(self):
        data = {
            'dn': 'mydn',
            'name_parts': 'a',
        }
        serializer = SuggestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['name_parts'], ['Expected a list of items but got type "str".'])

    def test_required_fields(self):
        serializer = SuggestionSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['name_parts'], ['This field is required.'])


class UniqnameSerializerTests(SimpleTestCase):

    def test_valid_data(self):
        uid = 'megaman'
        data = {'uid': uid}
        serializer = UniqnameSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['uid'], uid)

    def test_invalid_data(self):
        uid = 'abc123'
        data = {'uid': uid}
        serializer = UniqnameSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['uid'], ['Enter a valid uniqname.'])

    def test_required_fields(self):
        serializer = UniqnameSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['uid'], ['This field is required.'])


class PasswordSerializerTests(SimpleTestCase):

    def test_valid_data(self):
        uid = 'megaman'
        password1 = 'mypass'
        password2 = 'mypass'
        data = {
            'uid': uid,
            'password1': password1,
            'password2': password2,
        }
        serializer = PasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['uid'], uid)
        self.assertEqual(serializer.validated_data['password1'], password1)
        self.assertEqual(serializer.validated_data['password2'], password2)

    def test_invalid_data(self):
        uid = 'abc123'
        password1 = 'mypass'
        data = {
            'uid': uid,
            'password1': password1,
        }
        serializer = PasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['uid'], ['Enter a valid uniqname.'])

    def test_required_fields(self):
        serializer = PasswordSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['uid'], ['This field is required.'])
        self.assertEqual(serializer.errors['password1'], ['This field is required.'])

