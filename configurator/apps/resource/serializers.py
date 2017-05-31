from rest_framework import serializers
from .models import *
from configurator.apps.http_resource.models import HTTPResource


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        exclude = ('polymorphic_ctype', "id",)

    def to_representation(self, obj):
        """
        Because Resource is Polymorphic
        """
        if isinstance(obj, StringResource):
            return StringSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, IntResource):
            return IntSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, ListResource):
            return ListSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, DictResource):
            return DictSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, HTTPResource):
            return HttpSerializer(obj, context=self.context).to_representation(obj)
        return super(ResourceSerializer, self).to_representation(obj)


class StringSerializer(serializers.ModelSerializer):
    # type_name = "string"
    type = serializers.CharField(read_only=True, source='type_name')
    value = serializers.CharField()
    # value = serializers.SlugRelatedField(
    # many=False, slug_field='value', read_only=True)

    class Meta:
        model = StringResource
        exclude = ('polymorphic_ctype', "id",)


class IntSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type_name')
    value = serializers.IntegerField()

    class Meta:
        model = IntResource
        exclude = ('polymorphic_ctype', "id",)


class DictEntrySerializer(serializers.ModelSerializer):
    value = ResourceSerializer()

    class Meta:
        model = DictResourceEntry
        exclude = ('dictionary', 'id',)


class DictSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True, source='type_name')
    entries = DictEntrySerializer(many=True)

    class Meta:
        model = DictResource
        exclude = ('polymorphic_ctype',)


class ListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True, source='type_name')
    value = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = ListResource
        exclude = ('polymorphic_ctype',)
        depth = 10


class HttpSerializer(serializers.ModelSerializer):
    # zrobić refa z pola app

    class Meta:
        model = HTTPResource
        exclude = ('polymorphic_ctype',)
        depth = 1
