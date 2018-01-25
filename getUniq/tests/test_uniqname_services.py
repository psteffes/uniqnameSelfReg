from django.test import SimpleTestCase
from ..uniqname_services import get_suggestions, find_uniqname, create_uniqname, reactivate_uniqname, reset_password, UniqnameServicesError

import random
import string
import logging


class UniqnameServicesTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)
        #pass

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Make sure we get suggestions back
    def test_get_suggestions(self):
        dn = 'umichDirectoryID=161-0700-20171005021110588-585,ou=Identities,o=Registry'
        name_parts = ['John', 'Doe']
        result = get_suggestions(dn, name_parts)
        self.assertTrue(len(result) > 2)

    # uniqname 'test' should exist
    def test_find_uniqname(self):
        uid = 'test'
        result = find_uniqname(uid)
        self.assertEqual(result, uid)

    # uniqname 'abc123' should not exist
    def test_uniqname_not_found(self):
        uid = 'test123'
        result = find_uniqname(uid)
        self.assertEqual(result, None)

    # Do not want to test successful create
    def test_failed_create(self):
        dn = 'umichDirectory=999,ou=Identities,o=Registry'
        uid = 'test123'
        umid = '99999955'
        with self.assertRaises(UniqnameServicesError) as context:
            create_uniqname(dn, uid, umid)
        self.assertEqual(context.exception.message, 'Uniqname create failed')

    # Do not want to test successful reactivate
    def test_failed_reactivate(self):
        dn = 'umichDirectory=999,ou=Identities,o=Registry'
        umid = '99999955'
        with self.assertRaises(UniqnameServicesError) as context:
            reactivate_uniqname(dn, umid)
        self.assertEqual(context.exception.message, 'Uniqname reactivation failed')

    # Test both successful and failed password change
    def test_password_change(self):
        # Generate a random password
        pw = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(55))
        # Test success
        reset_password('stesting', pw)    # Will raise an error if it fails

        # Test failure
        with self.assertRaises(UniqnameServicesError) as context: 
            reset_password('test123', pw)
        self.assertEqual(context.exception.message, 'passwordReset failed')

