from django.test import SimpleTestCase
from ..aws_sqs import add_message_to_queue

import logging


class SQSTests(SimpleTestCase):

    # Disable logging
    def setUp(self):
        logging.disable(logging.CRITICAL)

    # Reenable logging
    def tearDown(self):
        logging.disable(logging.NOTSET)

    # Add a message to the queue. Will raise error on failure
    def test_add_message(self):
        uid = 'thisisatest'
        email = 'fake@fakemail.com'
        response = add_message_to_queue(uid, email)
