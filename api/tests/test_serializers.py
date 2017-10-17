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
        name_parts = ('mega', 'man')
        data = {
            'dn': dn,
            'name_parts': name_parts,
        }
        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
