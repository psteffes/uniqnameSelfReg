from django.test import SimpleTestCase
from ..utils import getuniq_eligible, validate_passwords_final

import logging


class UtilTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Test eligible entry
    def test_eligible(self):
        entry = {
            'umichGetUniqStatus': ['ELIGIBLE'],
            'umichGetUniqEntitlingRoles': ['StudentAA'],
        }
        self.assertTrue(getuniq_eligible(entry))

    # Test inelgible entry
    def test_ineligible(self):
        entry = {
            'umichGetUniqStatus': 'INELIGIBLE',
        }
        self.assertFalse(getuniq_eligible(entry))
        self.assertFalse(getuniq_eligible({}))

    # Test valid passwords
    def test_valid_pw(self):
        uid = 'test'
        pw1 = '<Sup3r%S3cret!@_[]%'
        pw2 = '<Sup3r%S3cret!@_[]%'
        self.assertTrue(validate_passwords_final(uid, pw1, pw2))

    # Test invalid passwords
    def test_invalid_pw(self):
        uid = 'test'
        pw1 = 'secret1'
        pw2 = 'secret2'
        self.assertFalse(validate_passwords_final(uid, pw1, pw2))

