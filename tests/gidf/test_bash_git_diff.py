import pytest
from unittest.mock import patch

from gitbro.gidf.BashGitDiff import BashGitDiff
from gitbro.gidf import main as gidf_main


@pytest.fixture(autouse=True)
def reset_bash_git_diff_state():
    BashGitDiff.line = '{base} {action} {flags} {target}'
    BashGitDiff.base = 'git'
    BashGitDiff.action = 'diff'
    BashGitDiff.flags = []
    BashGitDiff.target = ''
    yield
    BashGitDiff.line = '{base} {action} {flags} {target}'
    BashGitDiff.base = 'git'
    BashGitDiff.action = 'diff'
    BashGitDiff.flags = []
    BashGitDiff.target = ''


@pytest.fixture
def run_gidf(monkeypatch):
    def _factory(argv, *, changed='src/file.py', queued='src/staged.py'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('gitbro.gidf.BashGitDiff.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_changed_files_for_diff.return_value = changed
            list_results_mock.return_value.find_queued_files_for_diff.return_value = queued

            instance = BashGitDiff()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitDiffCommands:
    def test_no_arguments_defaults_to_stat(self, run_gidf):
        result = run_gidf(['gidf'])

        assert result['system'] == ['git diff --stat']

    def test_all_option(self, run_gidf):
        result = run_gidf(['gidf', '-a'])

        assert result['system'] == ['git diff HEAD']

    def test_diff_option(self, run_gidf):
        result = run_gidf(['gidf', '-d'])

        assert result['system'] == ['git diff --patch-with-stat']

    def test_stat_option(self, run_gidf):
        result = run_gidf(['gidf', '-s'])

        assert result['system'] == ['git diff --stat']

    def test_queued_option(self, run_gidf):
        result = run_gidf(['gidf', '-q'])

        assert result['system'] == ['git diff --staged']

    def test_partial_file_with_short_extension_suffix_wildcard(self, run_gidf):
        # Pattern is r'\.\w?$' — only a trailing dot plus at most one word char
        result = run_gidf(['gidf', 'file'], changed='src/file.c')

        assert result['system'] == ['git diff *src/file.c']
        result['list_results'].find_changed_files_for_diff.assert_called_once_with('file')

    def test_partial_file_with_longer_extension_gets_surrounding_wildcards(self, run_gidf):
        result = run_gidf(['gidf', 'file'], changed='src/file.py')

        assert result['system'] == ['git diff *src/file.py*']

    def test_partial_file_without_extension_gets_surrounding_wildcards(self, run_gidf):
        result = run_gidf(['gidf', 'file'], changed='src/file')

        assert result['system'] == ['git diff *src/file*']

    def test_queued_partial_file_uses_queued_lookup(self, run_gidf):
        result = run_gidf(['gidf', '-q', 'stage'], queued='src/staged.py')

        assert result['system'] == ['git diff --staged *src/staged.py*']
        result['list_results'].find_queued_files_for_diff.assert_called_once_with('stage')

    def test_all_with_partial_file_still_uses_changed_lookup(self, run_gidf):
        result = run_gidf(['gidf', '-a', 'file'], changed='src/file.py')

        assert result['system'] == ['git diff HEAD *src/file.py*']
        result['list_results'].find_changed_files_for_diff.assert_called()


class TestBashGitDiffEntryPoints:
    def test_go_instantiates_bash_git_diff(self):
        with patch.object(BashGitDiff, '__init__', return_value=None) as init_mock:
            BashGitDiff.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitDiff, 'go') as go_mock:
            gidf_main.run()

        go_mock.assert_called_once_with()
