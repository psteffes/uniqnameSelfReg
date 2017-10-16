from django.test import SimpleTestCase
from ..token import generate_confirmation_token, confirm_token


class TokenTests(SimpleTestCase):

    # Generate a token and then verify it
    def test_tokens(self):
        umid = '12345678'
        first_name = 'mega'
        last_name = 'man'
        data = {
            'umid': umid,
            'first_name': first_name,
            'last_name': last_name,
        }
        token = generate_confirmation_token(data)
        self.assertNotIsInstance(token, dict)
        self.assertRaises(TypeError, lambda: token['umid'])
        decrypted = confirm_token(token)
        self.assertEquals(decrypted['umid'], umid)
        self.assertEquals(decrypted['first_name'], first_name)
        self.assertEquals(decrypted['last_name'], last_name)
