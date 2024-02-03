from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from conf.settings import MEDIA_MAX_FILE_SIZE
from upload.models.file import File, ALLOWED_CONTENT_TYPES


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'uploaded_at', 'is_processed')
        extra_kwargs = {
            'file': {'required': True, 'max_length': 50, 'allow_empty_file': False, 'use_url': False},
            'uploaded_at': {'read_only': True},
            'is_processed': {'read_only': True}
        }

    def validate_file(self, file):
        if file.size > MEDIA_MAX_FILE_SIZE:
            raise serializers.ValidationError(_('File size is too large.'))
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
            # process_file.delay(file.id, content_type)
        return file
