from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .models import File, FilePart
from .serializers import FileSerializer, FilePartSerializer


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        file_obj = request.data['file']
        filename = file_obj.name
        user = request.user
        file = File(
            owner=user,
            name=filename,
            content=file_obj
        )
        file.save()

        return Response(status=204)


class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileRetrieveView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDestroyView(generics.DestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
