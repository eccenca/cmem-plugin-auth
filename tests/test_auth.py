"""Plugin tests."""

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from cmem.cmempy.workspace.projects.resources.resource import get_resource_response
from cmem_client.models.dataset import Dataset, DatasetData
from cmem_client.models.project import Project
from cmem_client.repositories.protocols.import_item import ImportConflictPolicy
from cmem_plugin_base.dataintegration.client import get_client
from cmem_plugin_base.testing import TestExecutionContext

needs_cmem = pytest.mark.skipif(
    os.environ.get("CMEM_BASE_URI", "") == "", reason="Needs CMEM configuration"
)

PROJECT_NAME = "auth_test_project"
DATASET_NAME = "sample_dataset"
RESOURCE_NAME = "sample_dataset.txt"
DATASET_TYPE = "text"


@pytest.fixture
def setup(tmp_path: Path) -> Generator[None, Any]:
    """Provide the DI build project incl. assets."""
    client = get_client(TestExecutionContext())

    project = Project(name=PROJECT_NAME)
    client.projects.create_item(project)

    dataset = Dataset(
        id=DATASET_NAME,
        project_id=PROJECT_NAME,
        data=DatasetData(type=DATASET_TYPE, parameters={"file": RESOURCE_NAME}),
    )
    client.datasets.create_item(dataset)

    resource_file = tmp_path / RESOURCE_NAME
    resource_file.write_text("auth plugin sample file.")
    client.files.import_item(
        path=resource_file,
        key=f"{PROJECT_NAME}:{RESOURCE_NAME}",
        on_conflict=ImportConflictPolicy.REPLACE,
    )
    yield None
    client.projects.delete_item(PROJECT_NAME)


@needs_cmem
@pytest.mark.usefixtures("setup")
def test_integration_placeholder() -> None:
    """Placeholder to write integration testcase with cmem"""
    with get_resource_response(PROJECT_NAME, RESOURCE_NAME) as response:
        assert response.text != ""


def test_dummy() -> None:
    """Dummy test to avoid pytest to run amok in case no cmem is available."""
