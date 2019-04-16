from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import AssetFile
from .serializers import AssetFileSerializer


class AssetFileViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,)
    serializer_class = AssetFileSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'owner': request.user.id,
            'content': request.data.get('file', None)
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_data = self.get_serializer(instance=instance)
        headers = self.get_success_headers(response_data.data)
        return Response(response_data.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        queryset = AssetFile.objects.filter(owner=self.request.user)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
