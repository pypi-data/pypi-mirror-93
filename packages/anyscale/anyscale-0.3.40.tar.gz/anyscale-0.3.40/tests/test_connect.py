from datetime import datetime
import os
from pathlib import Path
from typing import Any, List, Tuple
from unittest.mock import ANY, Mock

import pytest
import yaml

import anyscale
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.client.openapi_client.models.project_response import ProjectResponse  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.connect import SessionBuilder

UP_CMD = [
    "anyscale",
    "_up",
    "--config",
    "session-default.yaml",
    "--cloud-name",
    "anyscale_default_cloud",
]


def _make_session(i: int, state: str) -> Session:
    return Session(
        id="session_id",
        name="session-{}".format(i),
        created_at=datetime.now(),
        snapshots_history=[],
        idle_timeout=120,
        tensorboard_available=False,
        project_id="project_id",
        state=state,
        service_proxy_url="http://session-{}.userdata.com/auth?token=value&bar".format(
            i
        ),
    )


def _make_test_builder(
    tmp_path: Path, session_states: List[str] = ["Running"]
) -> Tuple[Any, Any, Any, Any]:
    scratch = tmp_path / "scratch"
    sdk = Mock()
    sess_resp = Mock()
    ray = Mock()
    api_mock = Mock()
    api_mock.connect.return_value = {"num_clients": 1}
    ray.util.client.RayAPIStub.return_value = api_mock
    ray.util.connect.return_value = {"num_clients": 1}
    sess_resp.results = [
        _make_session(i, state) for i, state in enumerate(session_states)
    ]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp
    subprocess = Mock()
    builder = SessionBuilder(
        scratch_dir=scratch.absolute().as_posix(),
        anyscale_sdk=sdk,
        subprocess=subprocess,
        ray=ray,
    )
    setattr(builder, "_up_session", Mock())
    return builder, sdk, subprocess, ray


def test_new_proj_connect_params(tmp_path: Path, project_test_data: Project) -> None:
    project_dir = (tmp_path / "my_proj").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file
    builder.project_dir(project_dir).connect()

    assert anyscale.project.get_project_id(project_dir)
    builder._up_session.assert_called_once_with(
        ANY, "session-0", project_dir,
    )

    # Also check connection params in this test.
    ray.util.connect.assert_called_once_with(
        "session-0.userdata.com:8081",
        metadata=[("cookie", "anyscale-token=value"), ("port", "10001")],
        secure=False,
        connection_retries=3,
    )


def test_detect_existing_proj(tmp_path: Path) -> None:
    nested_dir = (tmp_path / "my_proj" / "nested").absolute().as_posix()
    parent_dir = os.path.dirname(nested_dir)
    os.makedirs(nested_dir)
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)

    # Setup project in parent dir
    project_yaml = os.path.join(parent_dir, ".anyscale.yaml")
    with open(project_yaml, "w+") as f:
        f.write(yaml.dump({"project_id": 12345}))

    # Should detect the parent project dir
    cwd = os.getcwd()
    try:
        os.chdir(nested_dir)
        builder.connect()
    finally:
        os.chdir(cwd)

    builder._up_session.assert_called_once_with(
        ANY, "session-0", parent_dir,
    )


def test_fallback_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_new_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Should create a new session.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_base_docker_image(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)
    builder.project_dir(scratch_dir).base_docker_image(
        "anyscale/ray-ml:custom"
    ).connect()

    with open(
        (tmp_path / "scratch" / "session-default.yaml").absolute().as_posix()
    ) as f:
        data = yaml.safe_load(f)

    assert data["docker"]["image"] == "anyscale/ray-ml:custom"
    for nodes_type, node_config in data["available_node_types"].items():
        assert node_config["docker"]["image"] == "anyscale/ray-ml:custom"


def test_requirements_list(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Create a new session with a list of requirements.
    builder.project_dir(scratch_dir).require(["pandas", "wikipedia"]).connect()

    with open(
        (tmp_path / "scratch" / "session-default.yaml").absolute().as_posix()
    ) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia" | pip install -r /dev/stdin' in data["setup_commands"]
    )


def test_requirements_file(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    with open("/tmp/requirements.txt", "w") as f:
        f.write("pandas\nwikipedia\ndask")
    # Create a new session with a requiremetns file.
    builder.project_dir(scratch_dir).require("/tmp/requirements.txt").connect()

    with open(
        (tmp_path / "scratch" / "session-default.yaml").absolute().as_posix()
    ) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia\ndask" | pip install -r /dev/stdin'
        in data["setup_commands"]
    )


def test_new_session_lost_lock(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Emulate session lock failure.
    api_mock = Mock()
    api_mock.connect.return_value = {"num_clients": 9999999}
    ray.util.client.RayAPIStub.return_value = api_mock

    # Should create a new session.
    with pytest.raises(RuntimeError):
        builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_reuse_session_hash_match(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Create fake session-default.yaml for fingerprinting.
    os.makedirs(scratch_dir)
    builder.require(["wikipedia", "dask"]).project_dir(scratch_dir)
    cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
    builder._populate_cluster_config(cluster_yaml)
    with open(os.path.join(scratch_dir, "session-default.yaml"), "w+") as f:
        f.write(yaml.dump(cluster_yaml))
    local_files_hash = builder._fingerprint(scratch_dir).encode("utf-8")

    # Emulate session hash code match.
    api_mock = Mock()
    api_mock.connect.return_value = {"num_clients": 1}
    api_mock._internal_kv_get.return_value = local_files_hash
    ray.util.client.RayAPIStub.return_value = api_mock

    # Hash code match, no update needed.
    builder.require(["wikipedia", "dask"]).connect()

    builder._up_session.assert_not_called()

    # Hash code doesn't match, update needed.
    builder.require(["wikipedia", "dask", "celery"]).connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_reuse_session_hash_mismatch(
    tmp_path: Path, project_test_data: Project
) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    local_files_hash = b"wrong-hash-code"

    # Emulate session hash code mismatch.
    api_mock = Mock()
    api_mock.connect.return_value = {"num_clients": 1}
    api_mock._internal_kv_get.return_value = local_files_hash
    ray.util.client.RayAPIStub.return_value = api_mock

    # Should connect and run 'up'.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_reuse_session_lock_failure(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)
    api_mock = Mock()

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [
            _make_session(0, "Running"),
            _make_session(1, "Running"),
        ]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp
        api_mock.connect.return_value = {"num_clients": 1}

    builder._up_session.side_effect = create_session

    local_files_hash = builder._fingerprint(scratch_dir).encode("utf-8")

    # Emulate session hash code match but lock failure.
    api_mock.connect.return_value = {"num_clients": 9999}
    api_mock._internal_kv_get.return_value = local_files_hash
    ray.util.client.RayAPIStub.return_value = api_mock

    # Creates new session-1.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-1", scratch_dir,
    )


def test_restart_session_conn_failure(
    tmp_path: Path, project_test_data: Project
) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        raise ConnectionError("mock connect failure")

    # Emulate session hash code match but conn failure.
    api_mock = Mock()
    api_mock.connect.side_effect = fail_first_session
    ray.util.client.RayAPIStub.return_value = api_mock

    # Tries to restart it, but fails.
    with pytest.raises(ConnectionError):
        builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-0", scratch_dir,
    )


def test_skip_session_conn_failure(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        if "session-0" in url:
            raise ConnectionError("mock connect failure")
        else:
            return {"num_clients": 1}

    # Emulate session hash code match but conn failure.
    api_mock = Mock()
    api_mock.connect.side_effect = fail_first_session
    ray.util.client.RayAPIStub.return_value = api_mock

    # Skips session-0, updates session-1.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-1", scratch_dir,
    )


def test_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1", update=True).connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-1", scratch_dir,
    )


def test_fixed_session_no_update(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1", update=False).connect()

    builder._up_session.assert_not_called()


def test_new_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(i, "Running") for i in range(3)]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Should create a new session.
    builder.session("session-2").connect()

    builder._up_session.assert_called_once_with(
        ANY, "session-2", scratch_dir,
    )
