from rest_framework import serializers
from .models import *


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        exclude = ('polymorphic_ctype',)

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
        return super(ResourceSerializer, self).to_representation(obj)


class StringSerializer(serializers.ModelSerializer):
    # type_name = "string"
    type_name = serializers.CharField(read_only=True)
    value = serializers.CharField()
    # value = serializers.SlugRelatedField(
    # many=False, slug_field='value', read_only=True)

    class Meta:
        model = StringResource
        exclude = ('polymorphic_ctype',)


class IntSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)
    value = serializers.IntegerField()

    class Meta:
        model = IntResource
        exclude = ('polymorphic_ctype',)


class DictEntrySerializer(serializers.ModelSerializer):
    value = ResourceSerializer()

    class Meta:
        model = DictResourceEntry
        exclude = ('dictionary', 'id',)


class DictSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)
    entries = DictEntrySerializer(many=True)

    class Meta:
        model = DictResource
        exclude = ('polymorphic_ctype',)


class ListSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)
    value = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = ListResource
        exclude = ('polymorphic_ctype',)
        depth = 10
