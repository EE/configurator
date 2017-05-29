from rest_framework import viewsets
from .models import AppResource
from .serializers import AppSerializer


class AppViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AppResource.objects.all()
    serializer_class = AppSerializer
