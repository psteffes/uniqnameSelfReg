from django.test import SimpleTestCase
from django.urls import reverse
from ..views import terms, verify, confirm_email, create, password, success

import logging

class ViewsTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)
        #pass

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)


    # Terms
    def test_get_terms(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)

    def test_valid_post_terms(self):
        data = {'accept': True}
        response = self.client.post(reverse('terms'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/uniqname/verify/')

    def test_invalid_post_terms(self):
        data = {'bad': 'data'}
        response = self.client.post(reverse('terms'), data)
        self.assertEqual(response.status_code, 200)


    # This process requires a valid session, so we need to do it all in one big funciton
    # https://code.djangoproject.com/ticket/10899
    def test_through_confirm_email(self):
        # Terms
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)
        data = {'accept': True}
        response = self.client.post(reverse('terms'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/uniqname/verify/')
        session = self.client.session
        self.assertEqual(session['agreed_to_terms'], True)

        # Verify
        # GET the page
        response = self.client.get(reverse('verify'))
        self.assertEqual(response.status_code, 200)
        # Empty POST
        response = self.client.post(reverse('verify'))
        self.assertEqual(response.status_code, 200)
        # POST Unable to validate
        data = {
            'first_name': 'locked',
            'last_name': 'out',
            'birth_date': '05/05/5555',
            'umid': '55555555',
            'email': 'no@mail.com',
        }
        response = self.client.post(reverse('verify'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unable to validate identity', str(response.content))
        # POST Ineligble user
        data = {
            'first_name': 'locked',
            'last_name': 'out',
            'birth_date': '05/05/5555',
            'umid': '55555555',
            'email': 'no@mail.com',
        }
        #response = self.client.post(reverse('verify'), data)
        #self.assertEqual(response.status_code, 302)
        #self.assertIn('User is not eligible', response.content)
        # POST Eligible user
        data = {
            'first_name': 'suZie',
            'last_name': 'TESTeRs',
            'birth_date': '09/10/1980',
            'umid': '89109177',
            'email': 'stesters@noemail.com',
        }
        response = self.client.post(reverse('verify'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/uniqname/confirm_email/')
        session = self.client.session
        self.assertRaises(KeyError, lambda: session['agreed_to_terms'])
        self.assertEqual(session['email'], 'stesters@noemail.com')

        # confirm_email
        response = self.client.get(reverse('confirm_email'))
        self.assertEqual(response.status_code, 200)


    # New session can be used after confirming email, so lets start a new function
    def test_through_success(self):
        # Create
        data = {'umid': '89109177'}
        # Get the secure url through the API
        response = self.client.post(reverse('activation_link'), data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(response.json()['activation_link'])
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertTrue(session['dn'])
        self.assertTrue(session['roles'])
        # POST invalid data
        
