from rest_framework import serializers
from .models import *


class StringSerializer(serializers.ModelSerializer):
    # type_name = "string"
    type_name = serializers.CharField(read_only=True)
    # value = serializers.SlugRelatedField(
    # many=False, slug_field='value', read_only=True)

    class Meta:
        model = StringResource
        exclude = ('polymorphic_ctype',)


class IntSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = IntResource
        exclude = ('polymorphic_ctype',)
        depth = 1


class ListSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = ListResource
        exclude = ('polymorphic_ctype',)
        depth = 1


class DictSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = DictResource
        exclude = ('polymorphic_ctype',)
        depth = 1
