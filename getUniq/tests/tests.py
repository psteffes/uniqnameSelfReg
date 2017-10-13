from django.test import SimpleTestCase
from ..forms import AcceptForm, VerifyForm, UniqnameForm, PasswordForm

import datetime

# Create your tests here.


class AcceptFormTests(SimpleTestCase):

    # Test validation
    def test_valid_data(self):
        form = AcceptForm({'accept': True})
        self.assertTrue(form.is_valid())


    # Test for required fields
    def test_blank_data(self):
        form = AcceptForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['accept'], ['This field is required.'])

class VerifyFormTests(SimpleTestCase):

    # Test validation
    def test_valid_data(self):
        form = VerifyForm({
            'first_name': 'mega',
            'last_name': 'man',
            'birth_date': datetime.date(2000, 1, 1),
            'umid': '12345678',
            'email': 'megaman@mail.com',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'mega')
        self.assertEqual(form.cleaned_data['last_name'], 'man')
        self.assertEqual(form.cleaned_data['birth_date'], datetime.date(2000, 1, 1))
        self.assertEqual(form.cleaned_data['umid'], '12345678')
        self.assertEqual(form.cleaned_data['email'], 'megaman@mail.com')


    # Test for required fields
    def test_blank_data(self):
        form = VerifyForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['This field is required.'])
        self.assertEqual(form.errors['last_name'], ['This field is required.'])
        self.assertEqual(form.errors['birth_date'], ['This field is required.'])
        self.assertEqual(form.errors['umid'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])


    # Test for invalid data
    def test_invalid_data(self):
        form = VerifyForm({
            'first_name': 'mega',
            'last_name': 'man',
            'birth_date': 'not a birthdate',
            'umid': 'abc123',
            'email': 'noemail',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], ['Enter a valid date.'])
        self.assertEqual(form.errors['umid'], ['Enter a valid UMID.'])
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
