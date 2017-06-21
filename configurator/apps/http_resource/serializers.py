from configurator.apps.resource.serializers import ResourceModelSerializer
from .models import HTTPResource


class HttpSerializer(ResourceModelSerializer):
    type_name = 'http'
    # zrobić refa z pola app

    class Meta(ResourceModelSerializer.Meta):
        model = HTTPResource
