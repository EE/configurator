from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from configurator.apps.resource.models import *
import configurator.apps.resource.serializers as serializers


@api_view(['GET'])
def resource_list(request):
    """
    List all resources, or create a new snippet.
    """
    if request.method == 'GET':
        resources = [r for r in Resource.objects.all()
                     if hasattr(r, 'type_name')]

        result = {}
        for resource in resources:
            res_class_name = resource.type_name.title() + "Serializer"
            serializer = getattr(serializers, res_class_name)(
                resource, many=False)
            result[resource.name] = serializer.data

        print(result)
        return Response(result)
