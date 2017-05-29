from django.db import models

from configurator.apps.resource.models import Resource


class HTTPResource(Resource):
    """HTTP location of specified service

     *`app` is an application that provides this HTTP resource or NULL if
      resource is provided by external system.
     * `api` is a string identifying type (protocol) of this HTTP resource.
     * `host`, `port` and `path` specify location.
    """
    app = models.ForeignKey('application.AppResource', blank=True, null=True)
    api = models.CharField(max_length=200, blank=True)
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    path = models.CharField(max_length=1000)

    @property
    def requirements(self):
        return frozenset([self.app])

    @property
    def optional_requirements(self):
        return frozenset()

    @property
    def full_address(self):
        return 'http://{}:{}{}'.format(self.host, self.port, self.path)

    def to_rendering_context(self):
        return {
            'api': self.api,
            'host': self.host,
            'port': self.port,
            'path': self.path,
        }

    @property
    def docker_compose_link(self):
        if self.app is not None:
            return '{}:{}'.format(self.app.docker_service_name, self.host)
        else:
            # TODO
            raise Exception('not supported yet')
