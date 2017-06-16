from configurator.apps.resource.serializers import ResourceAbstractSerializer
from .models import HTTPResource


class HttpSerializer(ResourceAbstractSerializer):
    # zrobić refa z pola app

    class Meta(ResourceAbstractSerializer.Meta):
        model = HTTPResource
