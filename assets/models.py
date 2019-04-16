import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def asset_file_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.owner.id, filename)


def asset_file__part_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.asset_file.owner.id, filename)


class AssetFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    content = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mp3'])],
        upload_to=asset_file_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)


class AssetFilePart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_file = models.ForeignKey('AssetFile',related_name='asset_file_parts', on_delete=models.CASCADE)
    content = models.FileField(upload_to=asset_file__part_upload_path)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
