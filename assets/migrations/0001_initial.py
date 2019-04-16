import assets.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('content', models.FileField(upload_to=assets.models.asset_file_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mp3'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssetFilePart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.FileField(upload_to=assets.models.asset_file__part_upload_path)),
                ('order', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('asset_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_file_parts', to='assets.AssetFile')),
            ],
        ),
    ]
