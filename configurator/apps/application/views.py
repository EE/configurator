from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AppResource
from .serializers import AppSerializer


# class AppViewSet(viewsets.ModelViewSet):

#     API endpoint that allows users to be viewed or edited.

#     queryset = AppResource.objects.all()
#     serializer_class = AppSerializer


class AppList(APIView):
    """
    List all apps, or create a new app.
    """

    def get(self, request, format=None):
        apps = AppResource.objects.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppDetail(APIView):
    """
    Retrieve, update or delete an app instance.
    """

    def get_object(self, pk):
        try:
            return AppResource.objects.get(pk=pk)
        except AppResource.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AppSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AppSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
