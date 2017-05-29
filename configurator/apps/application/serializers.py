from rest_framework import serializers
from .models import AppResource


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppResource
        fields = '__all__'
        depth = 4
