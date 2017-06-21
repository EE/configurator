from rest_framework import serializers
from configurator.apps.resource.serializers import DictSerializer, ResourceModelSerializer
from .models import AppResource


class AppSerializer(ResourceModelSerializer):
    type_name = 'app'
    required_resource = DictSerializer()

    class Meta(ResourceModelSerializer.Meta):
        model = AppResource
