"""
Utils functions
"""
from django.conf import settings
from django.core.files import File as DjangoFile
from moviepy.tools import extensions_dict
from moviepy.editor import VideoFileClip, AudioFileClip
from .models import AssetFile, AssetFilePart


def generate_time_frames(clip_duration, frame_size):
    if (clip_duration % frame_size == 0):
        nparts = int(clip_duration / frame_size)
    else:
        nparts = int(clip_duration / frame_size) + 1

    breakpoints = [
        i * frame_size if i * frame_size < clip_duration else clip_duration
        for i in range(0, nparts + 1)
    ]

    time_frames = []
    for i in range(nparts):
        time_frame = (breakpoints[i], breakpoints[i+1])
        time_frames.append(time_frame)

    return time_frames


def save_file_and_audio_tracks(owner, content):
    filename = content.name[:content.name.rfind('.')]
    extension = content.name[content.name.rfind('.')+1:]

    content_tempfile_path = '{temp_dir}{filename}.{extension}'.format(
        temp_dir=settings.FILE_UPLOAD_TEMP_DIR,
        filename=filename,
        extension=extension)

    with open(content_tempfile_path, 'wb+') as destination:
        destination.write(content.read())

    clip_type = extensions_dict[extension]['type']
    if clip_type == 'video':
        audio = VideoFileClip(content_tempfile_path).audio
    elif clip_type == 'audio':
        audio = AudioFileClip(content_tempfile_path)

    asset_file = AssetFile(owner=owner, content=content, name=content.name)
    asset_file.save()

    time_frames = generate_time_frames(
        clip_duration=audio.duration,
        frame_size=settings.ASSETS_ASSET_FILE_PART_SIZE)

    for part_number, frame in enumerate(time_frames, start=1):
        audio_clip_part = audio.subclip(*frame)

        audio_path = '{temp_dir}{filename}_{part_number}.{extension}'.format(
            temp_dir=settings.FILE_UPLOAD_TEMP_DIR,
            filename=filename,
            part_number=part_number,
            extension='mp3')

        audio_clip_part.write_audiofile(audio_path)

        with open(audio_path, 'rb') as audio_file:
            file_content = DjangoFile(audio_file)
            file_part = AssetFilePart(asset_file=asset_file, order=part_number)
            file_part.content.save(audio_path, file_content)
            file_part.save()

    return asset_file
