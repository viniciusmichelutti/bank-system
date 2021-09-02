import ujson
from django.test import Client
from django.test.testcases import TestCase


class EventAPIViewTests(TestCase):
    def setUp(self):
        self.path = '/event'
        self.client = Client()

    def test_post_event_api_view(self):
        data = {'type': 'deposit', 'destination': '100', 'amount': 10}

        response = self.client.post(self.path, data, content_type='application/json')

        self.assertEqual(201, response.status_code)
        expected = {'destination': {'id': '100', 'balance': 10}}
        self.assertEqual(expected, ujson.loads(response.content))

    def test_post_event_api_view_with_non_existing_account(self):
        data = {'type': 'withdraw', 'origin': '200', 'amount': 10}

        response = self.client.post(self.path, data, content_type='application/json')

        self.assertEqual(404, response.status_code)
