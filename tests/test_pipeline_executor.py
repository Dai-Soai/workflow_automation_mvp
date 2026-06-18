from workflow_automation.pipeline_executor import PipelineExecutionResult


def test_pipeline_execution_result_contract():
    result = PipelineExecutionResult(
        status="ok",
        command=["doc-pipe", "--batch", "data/input_docs"],
        stdout="Processed: 3",
        stderr="",
        returncode=0,
    )

    assert result.status == "ok"
    assert result.command[0] == "doc-pipe"
    assert result.returncode == 0
