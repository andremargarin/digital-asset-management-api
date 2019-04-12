from django.db import transaction
from rest_framework import serializers
from .models import File, FilePart
from .utils import save_audio_tracks


class FilePartSerializer(serializers.ModelSerializer):

  class Meta:
    model = FilePart
    fields = ("id", "file", "content", "order")


class FileSerializer(serializers.ModelSerializer):

    file_parts = FilePartSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = ('id', 'owner', 'content', 'file_parts')

    @transaction.atomic
    def save(self):
        owner = self.validated_data.get('owner')
        content = self.validated_data.get('content')

        file = File(owner=owner, content=content, name=content.name)
        file.save()

        save_audio_tracks(file)
        return file
