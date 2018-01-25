from django.test import SimpleTestCase
from django.conf import settings
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from ..myldap import mcomm_reg_umid_search, set_status_complete

import logging


class searchTests(SimpleTestCase):

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


class updateStatusTests(SimpleTestCase):

    # Configure LDAP Connection
    server = Server(settings.LDAP_URI)
    conn = Connection(server, settings.LDAP_USERNAME, settings.LDAP_PW, auto_bind=True)

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Set Status Complete
    def test_set_status_complete(self):
        dn = 'umichDirectoryID=161-0700-20171016024233439-535,ou=Identities,o=Registry'
        self.assertTrue(set_status_complete(dn))

