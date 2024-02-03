import pytest
from django.urls import reverse
from factory import create_batch

from upload.models.file import File
from upload.tests.factories.file_factory import FileFactory


@pytest.fixture
def url():
    return reverse("upload:files_list")


@pytest.fixture
def multiple_files():
    return create_batch(klass=File, FACTORY_CLASS=FileFactory, size=5)
