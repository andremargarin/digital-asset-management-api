"""
Utils functions
"""
from django.conf import settings
from django.core.files import File as DjangoFile
from moviepy.tools import extensions_dict
from moviepy.editor import VideoFileClip, AudioFileClip
from .models import File, FilePart


def get_filename_and_extension(filename):
    """
    TODO: refatorar
    os.path.basename(remix).rsplit('.')[0]
    """
    name = filename[:filename.rfind('.')]
    extension = filename[filename.rfind('.')+1:]
    return name, extension



def generate_time_frames(clip_duration, max_frame_size):
    if (clip_duration % max_frame_size == 0):
        nparts = int(clip_duration / max_frame_size)
    else:
        nparts = int(clip_duration / max_frame_size) + 1

    breakpoints = [
        i * max_frame_size if i * max_frame_size < clip_duration else clip_duration
        for i in range(0, nparts + 1)
    ]

    time_frames = []
    for i in range(nparts):
        time_frame = (breakpoints[i], breakpoints[i+1])
        time_frames.append(time_frame)

    return time_frames


def save_temp_file(file):
    tempfile_path = '/tmp/' + file.name
    with open(tempfile_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return tempfile_path

def save_audio_tracks(file):

    content = file.content.instance
    filename, extension = get_filename_and_extension(content.name)
    clip_type = extensions_dict[extension]['type']

    if clip_type == 'video':
        audio = VideoFileClip(file.content.path).audio
    elif clip_type == 'audio':
        audio =  AudioFileClip(file.content.path)

    audio_clip_time_frames = generate_time_frames(audio.duration, 50)

    for part_number, frame in enumerate(audio_clip_time_frames, start=1):

        audio_clip_part = audio.subclip(*frame)

        file_part_name = '{filename}_{part_number}.{extension}'.format(
            filename=filename,
            part_number=part_number,
            extension='mp3'
        )

        audio_clip_part.write_audiofile(settings.MEDIA_ROOT + file_part_name)

        file_part = FilePart(file=file, order=part_number, content=file_part_name)
        file_part.save()
