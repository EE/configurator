from django.test import TestCase
from configurator.apps.resource.tests import SerializerTestMixin
from .models import HTTPResource

class HttpSerializerTest(TestCase, SerializerTestMixin):

    def setUp(self):
        self.some_http_endpoint = HTTPResource.objects.create(
            name='quantum data store access',
            api='quantum-store',
            host='10.52.0.7',
            port=1337,
            path='/api'
        )

    def test_serializer(self):
        o = self.some_http_endpoint
        self.assert_serializer_output(
            o,
            {
                'app': o.app,
                'api': o.api,
                'host': o.host,
                'port': o.port,
                'path': o.path,
            }
        )
