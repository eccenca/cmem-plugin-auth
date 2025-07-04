"""Plugin tests."""

import io
import os
from collections.abc import Generator
from typing import Any

import pytest
from cmem.cmempy.workspace.projects.datasets.dataset import make_new_dataset
from cmem.cmempy.workspace.projects.project import delete_project, make_new_project
from cmem.cmempy.workspace.projects.resources.resource import (
    create_resource,
    get_resource_response,
)

needs_cmem = pytest.mark.skipif(
    os.environ.get("CMEM_BASE_URI", "") == "", reason="Needs CMEM configuration"
)

PROJECT_NAME = "auth_test_project"
DATASET_NAME = "sample_dataset"
RESOURCE_NAME = "sample_dataset.txt"
DATASET_TYPE = "text"


@pytest.fixture
def setup() -> Generator[None, Any, None]:
    """Provide the DI build project incl. assets."""
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
    yield None
    delete_project(PROJECT_NAME)


@needs_cmem
@pytest.mark.usefixtures("setup")
def test_integration_placeholder() -> None:
    """Placeholder to write integration testcase with cmem"""
    with get_resource_response(PROJECT_NAME, RESOURCE_NAME) as response:
        assert response.text != ""


def test_dummy() -> None:
    """Dummy test to avoid pytest to run amok in case no cmem is available."""
