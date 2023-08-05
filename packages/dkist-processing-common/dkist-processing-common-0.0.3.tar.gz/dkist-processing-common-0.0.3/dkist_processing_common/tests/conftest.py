"""
Global test fixtures
"""
from pathlib import Path
from random import randint
from typing import Tuple

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common._util.tags import TagDB
from dkist_processing_common.base import SupportTaskBase


@pytest.fixture(scope="session")
def support_task():
    """
    Create task class for usage in tests
    """

    class TaskClass(SupportTaskBase):
        def run(self) -> None:
            pass

    return TaskClass(recipe_run_id=1, workflow_name="workflow_name", workflow_version="version")


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def tag_db(recipe_run_id) -> TagDB:
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags")
    yield t
    t.purge()
    t.close()


@pytest.fixture()
def tag_db2(recipe_run_id) -> TagDB:
    """
    Another instance of a tag db in the same redis db
    """
    recipe_run_id = recipe_run_id + 15  # same db number but different namespace
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags2")
    yield t
    t.purge()
    t.close()


@pytest.fixture(params=[None, "use_tmp_path"])
def workflow_file_system(request, recipe_run_id, tmp_path) -> Tuple[WorkflowFileSystem, int, Path]:
    if request.param == "use_tmp_path":
        path = tmp_path
    else:
        path = request.param
    wkflow_fs = WorkflowFileSystem(
        recipe_run_id=recipe_run_id,
        task_name="wkflow_fs_test",
        scratch_base_path=path,
    )
    yield wkflow_fs, recipe_run_id, tmp_path
    wkflow_fs.purge()
    tmp_path.rmdir()
    wkflow_fs.close()
