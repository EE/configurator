from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from configurator.apps.resource.models import *
import configurator.apps.resource.serializers as serializers
from rest_framework.views import APIView
from rest_framework.response import Response


class ResourceList(APIView):
    """
    List all resources, or create a new resource.
    """

    def get(self, request, format=None):
        resources = Resource.objects.all()
        result = []
        for resource in resources:
            serializer = resource.serializer()(resource, many=False)
            result.append(serializer.data)
        return Response(result)

    def post(self, request, format=None):
        serializer = serializers.ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResourceDetail(APIView):
    """
    Retrieve, update or delete a resource instance.
    """

    def get_object(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except AppResource.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.ResourceSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.ResourceSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
