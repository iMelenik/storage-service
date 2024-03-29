from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from conf.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from upload.models.file import File, ALLOWED_CONTENT_TYPES
from utils.serializer.fields import IntToDateTimeField
from .tasks import process_file


class FileSerializer(serializers.ModelSerializer):
    uploaded_at = IntToDateTimeField(read_only=True)

    class Meta:
        model = File
        fields = ('file', 'uploaded_at', 'is_processed')
        extra_kwargs = {
            'file': {'required': True, 'max_length': 50, 'allow_empty_file': False, 'use_url': False},
            'is_processed': {'read_only': True}
        }

    def validate_file(self, file):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise serializers.ValidationError(_(
                    'File size is too large. At most {} bytes are allowed').format(FILE_UPLOAD_MAX_MEMORY_SIZE))
        return file

    def validate(self, attrs):
        file = attrs.get('file')
        content_mime = file._name.split('.')[-1]
        for content_type, content_type_mimes in ALLOWED_CONTENT_TYPES.items():
            if content_mime in content_type_mimes:
                attrs['content_type'] = content_type
        if 'content_type' not in attrs:
            raise serializers.ValidationError(_('Unsupported file type.'))
        return attrs

    def save(self, **kwargs):
        content_type = self.validated_data.pop('content_type')
        with transaction.atomic():
            file = super().save(**kwargs)
            process_file.delay(file.id, content_type)
        return file
