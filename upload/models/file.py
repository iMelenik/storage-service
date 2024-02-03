import os

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

ALLOWED_CONTENT_TYPES = {
    'audio': ['mp3', 'mp4', 'aac'],
    'image': ['jpg', 'jpeg', 'png', 'gif'],
    'text': ['doc', 'docx', 'txt'],
}


class File(models.Model):
    """
    Table storing files, upload datetime and process status.
    """
    file = models.FileField(null=False, verbose_name=_('File'))
    uploaded_at = models.DateTimeField(auto_now_add=True, null=False, verbose_name=_('Uploaded at'))
    is_processed = models.BooleanField(default=False, null=False, verbose_name=_('Is processed'))

    objects = models.Manager()

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.file.name


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when File object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
