from django.test import TestCase
from django.test import Client
from .models import *
from django.core.management import call_command


class SerializerTestMixin:

    def assert_serializer_output(self, obj, output):
        d = output
        d.update({
            'type': obj.type_name,
            'id': obj.pk,
            'name': obj.name,
            'description': obj.description,
        })
        self.assertEqual(obj.serializer()(obj).data, d)


class APITest(TestCase):

    def setUp(self):
        call_command('loaddata', 'test', verbosity=0)
        self.sr = StringResource.objects.create(
            name="test", description="test descr", value="test2")
        self.ir = IntResource.objects.create(
            name="testInt", description="test descr", value=8080)

    def test_resource_get(self):
        # Issue a GET request.
        response = self.client.get('/api/resource/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            b'"testInt"' in response.content, True)


class ListResourceTest(TestCase):

    def test_empty_list(self):
        l = ListResource.objects.create(name='test list')
        l.full_clean()
        self.assertEqual(len(l.value.all()), 0)
