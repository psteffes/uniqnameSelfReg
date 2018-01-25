from django.test import SimpleTestCase
from ..idproof import idproof_form_data

import datetime
import logging


class IDProofTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test requests to id-verification-api
    def test_match(self):
        data = {
            'first_name': 'suZIe',    # case insensitivity
            'last_name': 'TESTers',
            'birth_date': datetime.date(1980, 9, 10),
            'umid': '89109177',
            'email': 'stesters@noemail.com',
        }
        result = idproof_form_data(data)
        self.assertIn(result['umichRegEntityID'][0], '89109177')

    # Test a failed match
    def test_no_match(self):
        data = {
            'first_name': 'LoCkEd',
            'last_name': 'oUt',
            'birth_date': datetime.date(5555, 5, 5),
            'umid': '55555555',
            'email': 'no@mail.com',
        }
        result = idproof_form_data(data)
        self.assertEqual(result, False)

