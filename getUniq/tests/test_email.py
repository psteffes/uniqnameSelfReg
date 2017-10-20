from django.test import SimpleTestCase
from ..email import send_confirm_email


class EmailTests(SimpleTestCase):

    # Send the email to fakemail. Will raise an error on failure
    def test_email(self):
        send_confirm_email(
            'uniqnameSelfRegUnitTest@umich.edu',
            'mega',
            'man',
            'secureurl.com',
        )
