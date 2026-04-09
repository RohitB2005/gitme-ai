import pytest
from unittest.mock import patch, MagicMock
from gitme.diff import get_staged_diff


def test_raises_outside_git_repo():
    mock = MagicMock()
    mock.returncode = 1
    with patch("subprocess.run", return_value=mock):
        with pytest.raises(EnvironmentError, match="git repository"):
            get_staged_diff()


def test_raises_when_nothing_staged():
    def fake_run(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = ""
        return m
    with patch("subprocess.run", side_effect=fake_run):
        with pytest.raises(ValueError, match="No staged changes"):
            get_staged_diff()


def test_returns_diff_string():
    def fake_run(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "diff --git a/foo.py b/foo.py\n+hello"
        return m
    with patch("subprocess.run", side_effect=fake_run):
        result = get_staged_diff()
        assert "diff" in result