from django.test import TestCase
from django.test import Client
from .models import *


class APITest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.sr = StringResource.objects.create(
            name="test", description="test descr", value="test2")
        self.client = Client()
        response = self.client.get('/api/resource/')
        print(response.status_code)
        print(response.content)

    def test_resource_get(self):
        # Issue a GET request.
        response = self.client.get('/api/resource/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.content, b'{"test":{"type":"string","value":"test2","description":"test descr"}}')
