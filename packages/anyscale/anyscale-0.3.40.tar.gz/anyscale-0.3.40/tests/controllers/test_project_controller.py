import os
from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client import Project  # type: ignore
from anyscale.client.openapi_client.models.project_list_response import (  # type: ignore
    ProjectListResponse,
)
from anyscale.controllers.project_controller import ProjectController
from anyscale.project import ProjectDefinition


@pytest.fixture()
def mock_api_client(project_test_data: Project) -> Mock:
    mock_api_client = Mock()

    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.return_value = ProjectListResponse(
        results=[project_test_data]
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value.results = []
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.return_value.result.config = (
        ""
    )

    return mock_api_client


def test_clone_project(project_test_data: Project, mock_api_client: Mock) -> None:
    project_controller = ProjectController(api_client=mock_api_client)

    os_makedirs_mock = Mock(return_value=None)
    with patch.multiple("os", makedirs=os_makedirs_mock), patch(
        "anyscale.project._write_cluster_config_to_disk"
    ) as write_cluster_config_mock:
        project_controller.clone(project_name=project_test_data.name)

    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.assert_called_once_with(
        name=project_test_data.name,
    )
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.assert_called_once_with(
        project_test_data.id,
    )
    os_makedirs_mock.assert_called_once_with(project_test_data.name)
    write_cluster_config_mock.assert_called_once_with(
        project_test_data.id, "", project_test_data.name
    )


@pytest.mark.parametrize("config", [None, "tmp.yaml"])
def test_init_project(
    project_test_data: Project, mock_api_client: Mock, config: str
) -> None:
    project_controller = ProjectController(api_client=mock_api_client)
    project_definition = ProjectDefinition(os.getcwd())
    project_definition.config["name"] = project_test_data.name
    mock_create_new_proj_def = Mock(
        return_value=(project_test_data.name, project_definition)
    )
    mock_register_project = Mock()
    mock_validate_cluster_configuration = Mock()

    with patch.multiple(
        "anyscale.controllers.project_controller",
        create_new_proj_def=mock_create_new_proj_def,
        register_project=mock_register_project,
        validate_cluster_configuration=mock_validate_cluster_configuration,
    ):
        project_controller.init(name=project_test_data.name, config=config)

    mock_create_new_proj_def.assert_called_once_with(
        project_test_data.name,
        config,
        api_client=mock_api_client,
        use_default_yaml=(not bool(config)),
    )
    mock_register_project.assert_called_once_with(project_definition, mock_api_client)

    if config:
        mock_validate_cluster_configuration.assert_called_once_with(
            config, api_instance=mock_api_client
        )
