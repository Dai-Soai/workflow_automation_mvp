import pytest

from workflow_automation.registry import (
    get_task_definition,
    get_task_registry,
    is_supported_task,
    list_task_types,
)


def test_get_task_registry():
    registry = get_task_registry()

    assert "detect" in registry
    assert "pipeline" in registry
    assert "publish" in registry


def test_is_supported_task():
    assert is_supported_task("detect") is True
    assert is_supported_task("pipeline") is True
    assert is_supported_task("publish") is True
    assert is_supported_task("unknown") is False


def test_get_task_definition():
    task = get_task_definition("pipeline")

    assert task.task_type == "pipeline"
    assert task.name == "Run Document Pipeline"


def test_get_task_definition_rejects_unknown_task():
    with pytest.raises(ValueError, match="Unsupported task type"):
        get_task_definition("unknown")


def test_list_task_types():
    task_types = list_task_types()

    assert task_types == ["detect", "pipeline", "publish"]
