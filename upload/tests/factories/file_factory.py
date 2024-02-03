import factory
from factory.django import DjangoModelFactory

from upload.models.file import File


class FileFactory(DjangoModelFactory):
    class Meta:
        model = File

    file = factory.django.FileField(filename="test.txt")
    uploaded_at = factory.Faker('date_time')
    is_processed = factory.Faker('boolean')
