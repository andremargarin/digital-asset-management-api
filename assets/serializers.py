from rest_framework import serializers
from .models import File, FilePart


class FilePartSerializer(serializers.ModelSerializer):

  class Meta:
    model = FilePart
    fields = ("id", "file", "content", "order")


class FileSerializer(serializers.ModelSerializer):

    file_parts = FilePartSerializer(many=True)

    class Meta:
        model = File
        fields = ('id', 'owner', 'name', 'content', 'file_parts')
