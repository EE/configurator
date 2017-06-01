from rest_framework import serializers
from configurator.apps.resource.serializers import DictSerializer, ResourceAbstractSerializer
from .models import AppResource


class AppSerializer(ResourceAbstractSerializer):
    type = None
    required_resource = DictSerializer()

    class Meta(ResourceAbstractSerializer.Meta):
        model = AppResource
