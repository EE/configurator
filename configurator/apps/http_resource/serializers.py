from rest_framework import serializers
from .models import HTTPResource


class HTTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = HTTPResource
        fields = '__all__'
        depth = 1
