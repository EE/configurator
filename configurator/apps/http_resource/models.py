from django.db import models

from configurator.apps.application.models import AppResource
from configurator.apps.resource.models import Resource


class HTTPResource(Resource):
    """HTTP location of specified service

     *`app` is an application that provides this HTTP resource or NULL if
      resource is provided by external system.
     * `api` is a string identifying type (protocol) of this HTTP resource.
     * `host`, `port` and `path` specify location.
    """
    app = models.ForeignKey(AppResource, blank=True, null=True)
    api = models.CharField(max_length=200, blank=True)
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    path = models.CharField(max_length=1000)

    @property
    def full_address(self):
        return 'http://{}:{}{}'.format(self.host, self.port, self.path)
