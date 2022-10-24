"""Plugin tests."""
import io

import pytest
from cmem.cmempy.config import (
    get_oauth_client_id,
    get_oauth_client_secret,
    get_oauth_token_uri,
)
from cmem.cmempy.workspace.projects.datasets.dataset import make_new_dataset
from cmem.cmempy.workspace.projects.project import delete_project, make_new_project
from cmem.cmempy.workspace.projects.resources.resource import (
    create_resource,
)
from oauthlib.oauth2 import BackendApplicationClient

from cmem_plugin_auth.workflow.auth import OAuth2
from .utils import needs_cmem, TestExecutionContext

PROJECT_NAME = "auth_test_project"
DATASET_NAME = "sample_dataset"
RESOURCE_NAME = "sample_dataset.txt"
DATASET_TYPE = "text"


@pytest.fixture
def setup(request):
    """Provides the DI build project incl. assets."""
    make_new_project(PROJECT_NAME)
    make_new_dataset(
        project_name=PROJECT_NAME,
        dataset_name=DATASET_NAME,
        dataset_type=DATASET_TYPE,
        parameters={"file": RESOURCE_NAME},
        autoconfigure=False,
    )
    with io.StringIO("auth plugin sample file.") as response_file:
        create_resource(
            project_name=PROJECT_NAME,
            resource_name=RESOURCE_NAME,
            file_resource=response_file,
            replace=True,
        )

    request.addfinalizer(lambda: delete_project(PROJECT_NAME))


@needs_cmem
def test_integration_placeholder(setup):
    """Placeholder to write integration testcase with cmem"""
    entities = OAuth2(
        oauth_grant_type=BackendApplicationClient.grant_type,
        oauth_token_url=get_oauth_token_uri(),
        oauth_client_id=get_oauth_client_id(),
        oauth_client_secret=get_oauth_client_secret(),
        user_name="",
        password="",
    ).execute(inputs=[], context=TestExecutionContext())

    assert len(entities.entities) == 1


def test_dummy():
    """Dummy test to avoid pytest to run amok in case no cmem is available."""
