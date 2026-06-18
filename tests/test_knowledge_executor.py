from workflow_automation.knowledge_executor import (
    KnowledgeIndexResult,
    KnowledgeSearchResult,
)


def test_knowledge_index_result_contract():
    result = KnowledgeIndexResult(
        status="ok",
        command=["radar-search", "index", "outputs/published_documents"],
        stdout="Indexed 3 document(s).",
        stderr="",
        returncode=0,
    )

    assert result.status == "ok"
    assert result.command[0] == "radar-search"
    assert result.returncode == 0


def test_knowledge_search_result_contract():
    result = KnowledgeSearchResult(
        status="ok",
        command=["radar-search", "search", "RADAR"],
        stdout="Found 1 result(s).",
        stderr="",
        returncode=0,
    )

    assert result.status == "ok"
    assert result.command[1] == "search"
    assert result.returncode == 0
