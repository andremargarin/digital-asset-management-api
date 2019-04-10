from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    content = models.FileField()


class FilePart(models.Model):
    file = models.ForeignKey('File', related_name='file_parts', on_delete=models.CASCADE)
    content = models.FileField()
    order = models.PositiveIntegerField()
