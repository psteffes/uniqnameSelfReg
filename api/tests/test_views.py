from django.test import SimpleTestCase
from django.urls import reverse
from ..views import activation_link, get_suggestions, find_uniqname, validate_password

import logging

class ActivationLinkTests(SimpleTestCase):
    
    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test GET not allowed
    def test_get(self):
        response = self.client.get(reverse('activation_link'))
        self.assertEqual(response.status_code, 405)

    # Test 400 on empty post
    def test_bad_request(self):
        response = self.client.post(reverse('activation_link'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['umid'], ['This field is required.'])

    # Test 200
    def test_valid_data(self):
        data = {
            'umid': '12345678',
            'first_name': 'suZIe',
            'last_name': 'TESTers',
        }
        response = self.client.post(reverse('activation_link'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['activation_link'])


class GetSuggestionsTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test GET not allowed
    def test_get(self):
        response = self.client.get(reverse('get_suggestions'))
        self.assertEqual(response.status_code, 405)

    # Test empty post (gives us back one ugly uniqname)
    def test_bad_request(self):
        data = {'name_parts': ''}
        response = self.client.post(reverse('get_suggestions'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['name_parts'], ['This field may not be blank.'])

    # Test 200
    def test_valid_data(self):
        data = {
            'name_parts': ('suZIe', 'TESTers'),
        }
        response = self.client.post(reverse('get_suggestions'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['suggestions'])


class FindUniqnameTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test GET not allowed
    def test_get(self):
        response = self.client.get(reverse('find_uniqname'))
        self.assertEqual(response.status_code, 405)

    # Test 400 on empty post
    def test_bad_request(self):
        response = self.client.post(reverse('find_uniqname'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['uid'], ['This field is required.'])

    # Test 200
    def test_valid_data(self):
        uid = 'rtested'
        data = {'uid': uid}
        response = self.client.post(reverse('find_uniqname'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['uid'], uid)


class ValidatePasswordTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test GET not allowed
    def test_get(self):
        response = self.client.get(reverse('validate_password'))
        self.assertEqual(response.status_code, 405)

    # Test 400 on empty post
    def test_bad_request(self):
        response = self.client.post(reverse('validate_password'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['uid'], ['This field is required.'])
        self.assertEqual(response.json()['password1'], ['This field is required.'])

    # Test 200
    def test_valid_data(self):
        # Weak password
        uid = 'rtested'
        password1 = 'mypass'
        password2 = 'mypass'
        data = {
            'uid': uid,
            'password1': password1,
            'password2': password2,
        }
        response = self.client.post(reverse('validate_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['evaluation']['valid'])

        # Strong password
        password1 = 'suP3rS3cret![]_%'
        password2 = 'suP3rS3cret![]_%'
        data = {
            'uid': uid,
            'password1': password1,
            'password2': password2,
        }
        response = self.client.post(reverse('validate_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['evaluation']['valid'])
