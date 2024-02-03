import pytest
from rest_framework import status as st
from syrupy.matchers import path_type

from upload.models.file import File
from upload.tasks import process_file
from upload.tests.conftest import FILE_MAPPING


@pytest.mark.django_db
def test_upload_file_no_data(no_auth_client, url, snapshot_json):
    response = no_auth_client.post(
            path=url,
            format="multipart",
    )
    assert response.status_code == st.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot_json


#
#
@pytest.mark.django_db
def test_upload_file_invalid_data(no_auth_client, url, snapshot_json):
    response = no_auth_client.post(
            path=url,
            format="multipart",
            data={"file": "some string"}
    )
    assert response.status_code == st.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot_json


@pytest.mark.django_db
def test_upload_file_invalid_file_name(no_auth_client, url, invalid_file_name, snapshot_json):
    response = no_auth_client.post(
            path=url,
            format="multipart",
            data={'file': invalid_file_name}
    )
    assert response.status_code == st.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot_json


@pytest.mark.django_db
def test_upload_file_invalid_file_content_type(no_auth_client, url, invalid_file_content_type, snapshot_json):
    response = no_auth_client.post(
            path=url,
            format="multipart",
            data={'file': invalid_file_content_type}
    )
    assert response.status_code == st.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot_json


@pytest.mark.django_db
def test_upload_file_invalid_data_too_large(no_auth_client, url, invalid_file_size, snapshot_json):
    response = no_auth_client.post(
            path=url,
            format="multipart",
            data={'file': invalid_file_size}
    )
    assert response.status_code == st.HTTP_400_BAD_REQUEST
    assert response.json() == snapshot_json


@pytest.mark.usefixtures("celery_app")
@pytest.mark.usefixtures("celery_worker")
@pytest.mark.django_db(transaction=True)
def test_upload_file_valid_data(no_auth_client, url, valid_file, snapshot_json, celery_app, celery_worker):
    response = no_auth_client.post(
            path=url,
            format="multipart",
            data={'file': valid_file},
    )
    assert response.status_code == st.HTTP_201_CREATED
    assert response.json() == snapshot_json(matcher=path_type(mapping=FILE_MAPPING))

    file = File.objects.all().last()
    assert not file.is_processed

    task = process_file.delay(file.id, 'text')
    task.wait()
    file.refresh_from_db()
    assert file.is_processed
