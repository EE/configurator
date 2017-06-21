import sys
from rest_framework import serializers
from .models import *
from configurator.apps.http_resource.models import HTTPResource
from functools import lru_cache


class ResourceAbstractSerializer:
    """Superclass for resoruce serializers. Subclasses should define
    `type_name` class property."""


class ResourceModelSerializer(serializers.ModelSerializer, ResourceAbstractSerializer):

    class Meta:
        exclude = ('polymorphic_ctype',)


def all_subclasses(cls):
        return cls.__subclasses__() + [
            g for s in cls.__subclasses__()
            for g in all_subclasses(s)
        ]


class ResourceSerializer(serializers.BaseSerializer):
    """Serializer for polymorphic resource. It routes real work to
    specialized serializers."""
    type_field_name = 'type'

    @classmethod
    @lru_cache(maxsize=None)
    def serializers_by_type_name(cls):
        return {
            serializer_class.type_name: serializer_class()
            for serializer_class in all_subclasses(ResourceAbstractSerializer)
            if hasattr(serializer_class, 'type_name')
        }

    def to_representation(self, obj):
        specialized_serializer = obj.serializer()()
        rep = specialized_serializer.to_representation(obj)
        rep[self.type_field_name] = specialized_serializer.type_name
        return rep

    def to_internal_value(self, data):
        type_name = data.get(self.type_field_name, None)
        specialized_serializer = self.serializers_by_type_name().get(type_name)

        # raise error if specialized serializer was not found
        if specialized_serializer is None:
            raise serializers.ValidationError({
                self.type_field_name: 'This field must contain one of: {}.'.format(
                    ', '.join(self.serializers_by_type_name().keys())
                ),
            })

        # Storing serializer is needed because of stateful implementation of
        #   BaseSerializer. We need to access serializer in `update()`/`create()`.
        return {
            'serializer': specialized_serializer,
            'data': specialized_serializer.to_internal_value(data),
        }

    def update(self, instance, validated_data):
        return validated_data['serializer'].update(instance, validated_data['data'])

    def create(self, validated_data):
        return self.create_polymorphic(validated_data)

    @classmethod
    def create_polymorphic(cls, validated_data):
        return validated_data['serializer'].create(validated_data['data'])


class RefResourceSerializer(serializers.Serializer, ResourceAbstractSerializer):
    type_name = 'ref'
    id = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all())

    def create(self, validated_data):
        return validated_data['id']


class StringSerializer(ResourceModelSerializer):
    type_name = 'string'
    value = serializers.CharField()

    class Meta(ResourceModelSerializer.Meta):
        model = StringResource


class IntSerializer(ResourceModelSerializer):
    type_name = 'int'
    value = serializers.IntegerField()

    class Meta(ResourceModelSerializer.Meta):
        model = IntResource


class DictEntrySerializer(serializers.ModelSerializer):
    value = ResourceSerializer()

    class Meta:
        model = DictResourceEntry
        exclude = ('dictionary', 'id',)


class DictSerializer(ResourceModelSerializer):
    type_name = 'dict'
    entries = DictEntrySerializer(many=True)

    class Meta(ResourceModelSerializer.Meta):
        model = DictResource


class ListSerializer(ResourceModelSerializer):
    type_name = 'list'
    value = ResourceSerializer(many=True)

    class Meta(ResourceModelSerializer.Meta):
        model = ListResource

    def create(self, validated_data):
        value = validated_data.pop('value')
        l = ListResource.objects.create(**validated_data)
        l.value.set([
            ResourceSerializer.create_polymorphic(v)
            for v in value
        ])
        return l

