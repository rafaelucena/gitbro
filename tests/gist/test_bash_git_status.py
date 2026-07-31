import pytest
from unittest.mock import patch

from gitbro.gist.BashGitStatus import BashGitStatus
from gitbro.gist import main as gist_main


@pytest.fixture(autouse=True)
def reset_bash_git_status_state():
    BashGitStatus.line = '{base} {action} {flags} {target}'
    BashGitStatus.base = 'git'
    BashGitStatus.action = 'status'
    BashGitStatus.flags = []
    BashGitStatus.target = ''
    yield
    BashGitStatus.line = '{base} {action} {flags} {target}'
    BashGitStatus.base = 'git'
    BashGitStatus.action = 'status'
    BashGitStatus.flags = []
    BashGitStatus.target = ''


@pytest.fixture
def run_gist(monkeypatch):
    def _factory(argv, *, changed='readme', untracked='newfile'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('gitbro.gist.BashGitStatus.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_changed_files_for_diff.return_value = changed
            list_results_mock.return_value.find_untracked_files_for_add.return_value = untracked

            instance = BashGitStatus()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitStatusCommands:
    def test_no_arguments_runs_plain_status(self, run_gist):
        result = run_gist(['gist'])

        assert result['system'] == ['git status']

    def test_short_option(self, run_gist):
        result = run_gist(['gist', '-s'])

        assert result['system'] == ['git status --short']

    def test_long_option(self, run_gist):
        result = run_gist(['gist', '-l'])

        assert result['system'] == ['git status --long']

    def test_untracked_option(self, run_gist):
        result = run_gist(['gist', '-u'])

        assert result['system'] == ['git status --untracked-files=normal']

    def test_tracked_option(self, run_gist):
        result = run_gist(['gist', '-t'])

        assert result['system'] == ['git status --untracked-files=no']

    def test_all_untracked_option(self, run_gist):
        result = run_gist(['gist', '-a'])

        assert result['system'] == ['git status --untracked-files=all']

    def test_branch_option_can_combine_with_short(self, run_gist):
        result = run_gist(['gist', '-s', '-b'])

        assert result['system'] == ['git status --short --branch']

    def test_partial_name_uses_changed_file_with_wildcards(self, run_gist):
        result = run_gist(['gist', 'read'], changed='readme.md')

        assert result['system'] == ['git status *readme.md']
        result['list_results'].find_changed_files_for_diff.assert_called_once_with(['read'])

    def test_partial_name_falls_back_to_untracked_when_unchanged(self, run_gist):
        result = run_gist(['gist', 'new'], changed=['new'], untracked='newfile.txt')

        assert result['system'] == ['git status *newfile.txt']
        result['list_results'].find_untracked_files_for_add.assert_called_once_with(['new'])

    def test_partial_name_without_extension_gets_surrounding_wildcards(self, run_gist):
        result = run_gist(['gist', 'read'], changed='readme')

        assert result['system'] == ['git status *readme*']


class TestBashGitStatusEntryPoints:
    def test_go_instantiates_bash_git_status(self):
        with patch.object(BashGitStatus, '__init__', return_value=None) as init_mock:
            BashGitStatus.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitStatus, 'go') as go_mock:
            gist_main.run()

        go_mock.assert_called_once_with()
