from django.db import transaction
from rest_framework import serializers
from .models import AssetFile, AssetFilePart
from .utils import save_file_and_audio_tracks


class AssetFilePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetFilePart
        fields = ('id', 'asset_file', 'content', 'order', 'created_at')


class AssetFileSerializer(serializers.ModelSerializer):
    asset_file_parts = AssetFilePartSerializer(many=True, read_only=True)

    class Meta:
        model = AssetFile
        fields = ('id', 'owner', 'content', 'created_at', 'asset_file_parts')

    @transaction.atomic
    def save(self):
        owner = self.validated_data.get('owner')
        content = self.validated_data.get('content')
        asset_file = save_file_and_audio_tracks(owner=owner, content=content)
        return asset_file
