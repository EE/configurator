import sys
from rest_framework import serializers
from .models import *
from configurator.apps.http_resource.models import HTTPResource


THIS_MODULE = sys.modules[__name__]


class ResourceAbstractSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True, source='type_name')

    class Meta:
        exclude = ('polymorphic_ctype',)


class ResourceSerializer(ResourceAbstractSerializer):
    type = None

    class Meta:
        model = Resource

    def to_representation(self, obj):
        """
        Because Resource is Polymorphic
        """
        if obj.serializer == "ResourceSerializer":
            return super(ResourceSerializer, self).to_representation(obj)
        else:
            return getattr(THIS_MODULE, obj.serializer)(obj, context=self.context).to_representation(obj)


class StringSerializer(ResourceAbstractSerializer):
    value = serializers.CharField()

    class Meta(ResourceAbstractSerializer.Meta):
        model = StringResource


class IntSerializer(ResourceAbstractSerializer):
    value = serializers.IntegerField()

    class Meta(ResourceAbstractSerializer.Meta):
        model = IntResource


class DictEntrySerializer(serializers.ModelSerializer):
    value = ResourceSerializer()

    class Meta:
        model = DictResourceEntry
        exclude = ('dictionary', 'id',)


class DictSerializer(ResourceAbstractSerializer):
    entries = DictEntrySerializer(many=True)

    class Meta(ResourceAbstractSerializer.Meta):
        model = DictResource


class ListSerializer(ResourceAbstractSerializer):
    value = ResourceSerializer(many=True, read_only=True)

    class Meta(ResourceAbstractSerializer.Meta):
        model = ListResource


class HttpSerializer(ResourceAbstractSerializer):
    # zrobić refa z pola app

    class Meta(ResourceAbstractSerializer.Meta):
        model = HTTPResource
