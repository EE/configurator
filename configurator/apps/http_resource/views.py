from rest_framework import viewsets
from .models import HTTPResource
from .serializers import HTTPSerializer


class HTTPResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HTTPResource.objects.all()
    serializer_class = HTTPSerializer
