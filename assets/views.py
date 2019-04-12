from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import File, FilePart
from .serializers import FileSerializer, FilePartSerializer


class FileUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = FileSerializer

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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileRetrieveView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDestroyView(generics.DestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
