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
    def test_required_data(self):
        form = AcceptForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['accept'], ['This field is required.'])


class VerifyFormTests(SimpleTestCase):

    # Test validation
    def test_valid_data(self):
        form = VerifyForm({
            'first_name': 'mega',
            'last_name': 'man',
            'birth_date': datetime.date(1750, 1, 1),    # old but valid date
            'umid': '00123400',    # Test zero trimming
            'email': 'megaman@mail.com',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'mega')
        self.assertEqual(form.cleaned_data['last_name'], 'man')
        self.assertEqual(form.cleaned_data['birth_date'], datetime.date(1750, 1, 1))
        self.assertEqual(form.cleaned_data['umid'], '00123400')
        self.assertEqual(form.cleaned_data['email'], 'megaman@mail.com')

    # Test for required fields
    def test_required_data(self):
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

    # Test minimum date
    def test_min_date(self):
        form = VerifyForm({
            'birth_date': datetime.date(1600, 1, 1),
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], ['Value must be 01/01/1700 or later.'])


class UniqnameFormTests(SimpleTestCase):

    # Test validation
    def test_valid_data(self):
        form = UniqnameForm({'uniqname': 'megaman'})
        self.assertTrue(form.is_valid())

    # Test for required fields
    def test_required_data(self):
        form = UniqnameForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['This field is required.'])

    # Test for invalid data
    def test_invalid_data(self):
        form = UniqnameForm({'uniqname': 'ab'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['Enter a valid uniqname.'])

        form = UniqnameForm({'uniqname': 'abcdefghijk'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['Enter a valid uniqname.'])

        form = UniqnameForm({'uniqname': 'abc123'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['Enter a valid uniqname.'])

        form = UniqnameForm({'uniqname': 'abc!!!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['Enter a valid uniqname.'])

        form = UniqnameForm({'uniqname': 'abcXYZ'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['uniqname'], ['Enter a valid uniqname.'])


class PasswordFormTests(SimpleTestCase):

    # Test validation
    def test_valid_data(self):
        pass1 = ' secret '    # Do not trim spaces
        pass2 = ' secret '
        form = PasswordForm({
            'password': pass1,
            'confirm_password': pass2,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], pass1)
        self.assertEqual(form.cleaned_data['confirm_password'], pass2)

    # Test for required fields
    def test_required_data(self):
        form = PasswordForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['This field is required.'])
        self.assertEqual(form.errors['confirm_password'], ['This field is required.'])

    # Test for invalid data
    def test_invalid_data(self):
        form = PasswordForm({
            'password': '1234',
            'confirm_password': 'abcd',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Passwords do not meet requirements.'])


