from django.test import TestCase, override_settings
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os
import shutil

from configurator.apps.application.models import AppResource, MountedFile
from configurator.apps.application.start import pre_start, env_entry
from configurator.apps.resource.models import DictResource, DictResourceEntry, StringResource
from configurator.apps.http_resource.models import HTTPResource


class MinimalServiceTestCase(TestCase):
    def setUp(self):
        self.service = AppResource.objects.create(
            name='for fun',
            required_resource=DictResource.objects.create(),
            image_name='aaaa',
        )

    def test_start(self):
        env = {}
        pre_start(env)
        self.service.start(env)

        self.assertEqual(env[env_entry], {
            'version': '3',
            'services': {
                self.service.docker_service_name: {
                    'image': 'aaaa',
                    'volumes': [],
                    'links': [],
                },
            },
        })


class CommandRenderTestCase(TestCase):
    def setUp(self):
        self.args_dict = DictResource.objects.create()
        DictResourceEntry.objects.create(
            dictionary=self.args_dict,
            key='fiction',
            value=StringResource.objects.create(name='fiction for nginx', value='nonsense<br/>')
        )

        self.service = AppResource.objects.create(
            name='a service',
            required_resource=self.args_dict,
            image_name='nginx',
            command='--fiction-command {{ fiction }}',
        )

    def test_start(self):
        env = {}
        pre_start(env)
        self.service.start(env)

        self.assertEqual(
            env[env_entry]['services'][self.service.docker_service_name]['command'],
            '--fiction-command nonsense<br/>'
        )


class LinksRenderTestCase(TestCase):
    def setUp(self):
        self.service = AppResource.objects.create(
            name='service',
            required_resource=DictResource.objects.create(),
            image_name='aaaa',
        )
        self.http_resource = HTTPResource.objects.create(
            name='endpoint served by a service',
            app=self.service,
            host='the-host-name',
            port=5001,
            path='/api/v0/',
            api='ipfs-api-v0',
        )

        self.args_dict = DictResource.objects.create()
        DictResourceEntry.objects.create(
            dictionary=self.args_dict,
            key='required_service',
            value=self.http_resource
        )

        self.service2 = AppResource.objects.create(
            name='second service',
            required_resource=self.args_dict,
            image_name='bbbb',
        )

    def test_start(self):
        env = {}
        pre_start(env)
        self.service2.start(env)

        self.assertEqual(
            env[env_entry]['services'][self.service2.docker_service_name]['links'],
            ['{}:the-host-name'.format(self.service.docker_service_name)]
        )

@override_settings(DOCKER_COMPOSE_DIR=tempfile.mkdtemp())
@override_settings(MOUNTED_FILES_TEMPLATES_DIR=tempfile.mkdtemp())
class FileRenderTestCase(TestCase):
    def setUp(self):
        self.args_dict = DictResource.objects.create()
        DictResourceEntry.objects.create(
            dictionary=self.args_dict,
            key='fiction',
            value=StringResource.objects.create(value='nonsense<br/>')
        )
        self.service = AppResource.objects.create(
            name='service',
            required_resource=self.args_dict,
            image_name='aaaa'
        )
        self.tpl = MountedFile.objects.create(
            app=self.service,
            mount_path='/etc/fiction.conf',
            file=SimpleUploadedFile('best_file_eva.txt', 'aaa {{fiction}} bbb'.encode('UTF-8'))
        )

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(settings.DOCKER_COMPOSE_DIR)
        shutil.rmtree(settings.MOUNTED_FILES_TEMPLATES_DIR)

    def test_start(self):
        env = {}
        pre_start(env)
        self.service.start(env)

        self.assertEqual(
            env[env_entry]['services'][self.service.docker_service_name]['volumes'],
            ['{}:/etc/fiction.conf:ro'.format(self.tpl.rendered_file_path)]
        )
        with open(os.path.join(
            settings.DOCKER_COMPOSE_DIR,
            self.tpl.rendered_file_path
        ), 'rt') as f:
            self.assertEqual(f.read(), 'aaa nonsense<br/> bbb')
