from django.db import models
from jinja2 import Environment
import os
from django.conf import settings

from configurator.apps.resource.models import Resource, DictResource
from configurator.apps.http_resource.models import HTTPResource
from configurator.apps.application.start import env_entry

template_engine = Environment(autoescape=False)


class AppResource(Resource):
    """An installed application."""
    required_resource = models.ForeignKey(
        DictResource,
        blank=True, null=True,
        related_name='required_by_apps'
    )

    image_name = models.CharField(max_length=200)
    command = models.CharField(max_length=400, blank=True, null=True)

    @property
    def requirements(self):
        return frozenset([self.required_resource])

    @property
    def optional_requirements(self):
        return frozenset()

    def start(self, env):
        context = self.required_resource.to_rendering_context()

        links = [
            r.docker_compose_link
            for r in self.required_resource.flatten()
            if isinstance(r, HTTPResource)
        ]

        service_description = {
            'image': self.image_name,
            'volumes': [f.render(context) for f in self.files.all()],
            'links': links,
        }

        if self.command is not None:
            service_description['command'] = template_engine\
                .from_string(self.command)\
                .render(context)

        env[env_entry]['services'][self.docker_service_name] = service_description

    @property
    def docker_service_name(self):
        return 'service-{}'.format(self.id)

    def __str__(self):
        return self.name


class MountedFile(models.Model):
    app = models.ForeignKey(AppResource, related_name='files')
    mount_path = models.CharField(max_length=300)
    file = models.FileField(upload_to=settings.MOUNTED_FILES_TEMPLATES_DIR)

    def render(self, context):
        """Render the file using given context. Return docker volume
        entry."""
        tpl = self.file.read().decode('UTF-8')

        with open(os.path.join(
            settings.DOCKER_COMPOSE_DIR,
            self.rendered_file_path
        ), 'w') as target_file:

            target_file.write(
                template_engine\
                    .from_string(tpl)\
                    .render(context)
            )

        return '{}:{}:ro'.format(self.rendered_file_path, self.mount_path)

    @property
    def rendered_file_path(self):
        """Where to store rendered file, relative to docker-compose.yml"""
        return os.path.join('./', str(self.id))

    def __str__(self):
        return '{}: {}'.format(self.app, self.mount_path)
