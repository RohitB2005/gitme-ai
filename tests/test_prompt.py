from gitme.prompt import build_prompt, SYSTEM_PROMPT


def test_build_prompt_contains_diff():
    diff = "diff --git a/foo.py b/foo.py\n+hello"
    result = build_prompt(diff)
    assert diff in result


def test_system_prompt_mentions_conventional_commits():
    assert "Conventional Commits" in SYSTEM_PROMPT


def test_system_prompt_lists_types():
    for t in ["feat", "fix", "refactor", "docs", "style", "test", "chore"]:
        assert t in SYSTEM_PROMPT