import pytest
from rest_framework import status as st
from syrupy.matchers import path_type

from upload.tests.conftest import FILE_MAPPING


@pytest.mark.django_db
def test_files_list_no_files(no_auth_client, url):
    response = no_auth_client.get(
            path=url,
            format="json",
    )
    assert response.status_code == st.HTTP_200_OK
    assert len(response.data.get("results")) == 0


@pytest.mark.django_db
def test_files_list_with_files(no_auth_client, url, multiple_files, snapshot_json):
    response = no_auth_client.get(
            path=url,
            format="json",
    )
    assert response.status_code == st.HTTP_200_OK
    assert len(response.data.get("results")) == 5
    assert response.data.get("results")[0] == snapshot_json(
            matcher=path_type(mapping=FILE_MAPPING)
    )
