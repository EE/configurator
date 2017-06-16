from django.test import TestCase
from django.test import Client
from .models import *
from django.core.management import call_command
from .serializers import ResourceSerializer

API_RESOURCE_URL = '/api/resource/'


class SerializerTestMixin:

    def assert_serializer_output(self, obj, output):
        d = output
        d.update({
            'type': obj.serializer().type_name,
            'id': obj.pk,
            'name': obj.name,
            'description': obj.description,
        })
        self.assertEqual(ResourceSerializer(obj).data, d)

    def create_resource(self, data):
        s =  ResourceSerializer(data=data)
        self.assertTrue(s.is_valid())
        return s.save()


class SerializerTestMixin:

    def assert_serializer_output(self, obj, output):
        d = output
        d.update({
            'type': obj.serializer().type_name,
            'id': obj.pk,
            'name': obj.name,
            'description': obj.description,
        })
        self.assertEqual(ResourceSerializer(obj).data, d)

    def create_resource(self, data):
        s =  ResourceSerializer(data=data)
        self.assertTrue(s.is_valid())
        return s.save()


class APITest(TestCase):

    def setUp(self):
        call_command('loaddata', 'test', verbosity=0)
        self.sr = StringResource.objects.create(
            name="test", description="test descr", value="test2")
        self.ir = IntResource.objects.create(
            name="testInt", description="test descr", value=8080)

    def test_resource_get(self):
        # Issue a GET request.
        response = self.client.get(API_RESOURCE_URL)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'"testInt"', response.content)

    def test_resource_post(self):
        self.assertEqual(StringResource.objects.filter(name='abcd').count(), 0)
        response = self.client.post(API_RESOURCE_URL, {'type': 'string', 'name': 'abcd', 'value': 'aaaa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(StringResource.objects.get(name='abcd').value, 'aaaa')

    def test_resource_post_error(self):
        response = self.client.post(API_RESOURCE_URL, {'type': 'string', 'name': 'abcd'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('value', response.json())

        response = self.client.post(API_RESOURCE_URL, {'type': 'nonsense', 'name': 'abcd', 'value': 'lol'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('type', response.json())


class RefSerializerTest(TestCase, SerializerTestMixin):

    def setUp(self):
        self.s = StringResource.objects.create(name='test string', value='aaaa?')

    def test_create(self):
        l = self.create_resource({
            'type': 'ref',
            'id': self.s.id,
        })
        self.assertIsInstance(l, StringResource)
        self.assertEqual(l.value, 'aaaa?')

    def test_create_invalid_id(self):
        s = ResourceSerializer(data={
            'type': 'ref',
            'id': 543,
        })
        self.assertFalse(s.is_valid())


class ListSerializerTest(TestCase, SerializerTestMixin):

    def test_create_empty(self):
        l = self.create_resource({
            'type': 'list',
            'name': 'test_list',
            'value': [],
        })
        self.assertIsInstance(l, ListResource)
        self.assertEqual(l.name, 'test_list')
        self.assertEqual(l.value.all().count(), 0)

    def test_create_nested(self):
        l = self.create_resource({
            'type': 'list',
            'name': 'base list',
            'value': [{
                'type': 'list',
                'name': 'nested test list',
                'value': [{
                    'type': 'list',
                    'name': 'nested2 test list',
                    'value': [],
                }],
            }],
        })
        self.assertEqual(
            l.value.all()[0]
             .value.all()[0]
             .value.all().count(), 0)


class DictSerializerTest(TestCase, SerializerTestMixin):

    def test_serialize(self):
        d = DictResource.objects.create(name='base')
        dd = DictResource.objects.create(name='nested')
        d.entries.create(key='k', value=dd)
        self.assert_serializer_output(d, {
            'name': 'base',
            'entries': {
                'k': {
                    'id': dd.pk,
                    'type': 'dict',
                    'name': 'nested',
                    'description': None,
                    'entries': {},
                },
            },
        })

    def test_create_empty(self):
        l = self.create_resource({
            'type': 'dict',
            'name': 'test_dict',
            'entries': {},
        })
        self.assertIsInstance(l, DictResource)
        self.assertEqual(l.name, 'test_dict')
        self.assertEqual(l.entries.all().count(), 0)

    def test_create_nested(self):
        l = self.create_resource({
            'type': 'dict',
            'name': '1',
            'entries': {
                'nested': {
                    'type': 'dict',
                    'name': '2',
                    'entries': {
                        'more_nested': {
                            'type': 'dict',
                            'name': '3',
                            'entries': {},
                        },
                    },
                },
            },
        })
        self.assertEqual(
            l.entries.all()[0].value
             .entries.all()[0].value
             .entries.all().count(), 0)
