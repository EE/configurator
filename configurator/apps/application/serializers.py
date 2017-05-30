from rest_framework import serializers
from configurator.apps.resource.serializers import DictSerializer
from .models import AppResource


class AppSerializer(serializers.ModelSerializer):
    required_resource = DictSerializer()

    class Meta:
        model = AppResource
        exclude = ('polymorphic_ctype',)
        depth = 4
