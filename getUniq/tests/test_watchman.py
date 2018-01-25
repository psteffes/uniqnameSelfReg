from django.test import SimpleTestCase
from django.urls import reverse


class WatchmanTests(SimpleTestCase):
    def test_health(self):
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)
