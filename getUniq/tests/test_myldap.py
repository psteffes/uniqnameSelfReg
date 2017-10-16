from django.test import SimpleTestCase
from ..myldap import mcomm_reg_umid_search

import logging


class ldapTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Perform a search
    def test_reg_umid_search(self):
        umid = '99999953'
        entry = mcomm_reg_umid_search(umid)
        self.assertEqual(entry['umichRegEntityID'][0], umid)
