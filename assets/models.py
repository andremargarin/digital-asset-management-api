from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class File(models.Model):
    # TODO: rename AssetFile
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    content = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4'])])


class FilePart(models.Model):
    # TODO: rename AssetFilePart
    file = models.ForeignKey('File', related_name='file_parts', on_delete=models.CASCADE)
    content = models.FileField()
    order = models.PositiveIntegerField()
