import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


@pytest.fixture
def url():
    return reverse("upload:upload_file")


@pytest.fixture
def invalid_file_name():
    file_content = "This is the content of the text file."
    file = SimpleUploadedFile(f"{str(1234567890) * 20}.txt", file_content.encode('utf-8'))
    return file


@pytest.fixture
def invalid_file_content_type():
    file_content = "This is the content of the text file."
    file = SimpleUploadedFile("test.abc", file_content.encode('utf-8'))
    return file


@pytest.fixture
def invalid_file_size():
    file_size = 10 * 1024 * 1024 + 1  # 10 MB + 1 byte
    file_content = os.urandom(file_size)  # Generate random content
    file = SimpleUploadedFile("large_file.txt", file_content)
    return file


@pytest.fixture
def valid_file():
    file_content = "This is the content of the text file."
    file = SimpleUploadedFile("test.txt", file_content.encode('utf-8'))
    return file
