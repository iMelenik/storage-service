import pytest
from rest_framework.test import APIClient
from syrupy.extensions.json import JSONSnapshotExtension

from upload.tasks import process_file

FILE_MAPPING = {
    "file": (str,),
    "uploaded_at": (int,),
    "is_processed": (bool,),
}


@pytest.fixture
def no_auth_client():
    return APIClient()


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)


@pytest.fixture()
def celery_parameters():
    return {"result_extended": True}


@pytest.mark.usefixtures("celery_app")
@pytest.mark.usefixtures("celery_worker")
@pytest.fixture(autouse=True)
def celery_register_tasks(celery_app):
    celery_app.register_task(process_file)
