from django.core.exceptions import ObjectDoesNotExist

from conf.celery import app
from upload.models.file import File
from utils.file_processors.audio_file_processor import process_audio_file
from utils.file_processors.image_file_processor import process_image_file
from utils.file_processors.text_file_processor import process_text_file


@app.task(retry=True, max_retries=3, default_retry_delay=60 * 5)
def process_file(file_id: int, content_type: str) -> None:
    """
    Process file by content type.
    """
    try:
        file = File.objects.get(pk=file_id)
    except ObjectDoesNotExist:
        return
    if file.is_processed:
        return
    match content_type:
        case 'audio':
            process_audio_file(file)
        case 'image':
            process_image_file(file)
        case 'text':
            process_text_file(file)
        case _:
            return
    file.is_processed = True
    file.save()
