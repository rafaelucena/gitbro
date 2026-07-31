import pytest
from unittest.mock import patch

from gitbro.gilg.BashGitLog import BashGitLog
from gitbro.gilg import main as gilg_main


PRETTY_FLAG = (
    "--pretty=format:'%C(yellow)%h%Creset|%C(red)%ad%Creset|%C(yellow)%an%Creset:%s' "
    "--date=format:'%Y-%m-%d %H:%M:%S'"
)


@pytest.fixture(autouse=True)
def reset_bash_git_log_state():
    BashGitLog.line = '{base} {action} {flags} {target}'
    BashGitLog.base = 'git'
    BashGitLog.action = 'log'
    BashGitLog.flags = []
    BashGitLog.target = ''
    yield
    BashGitLog.line = '{base} {action} {flags} {target}'
    BashGitLog.base = 'git'
    BashGitLog.action = 'log'
    BashGitLog.flags = []
    BashGitLog.target = ''


@pytest.fixture
def run_gilg(monkeypatch):
    def _factory(argv, *, compare_branch='develop'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('gitbro.gilg.BashGitLog.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_branch_by_partial.return_value = compare_branch

            instance = BashGitLog()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitLogCommands:
    def test_no_arguments_runs_plain_log(self, run_gilg):
        result = run_gilg(['gilg'])

        assert result['system'] == ['git log']

    def test_author_option(self, run_gilg):
        result = run_gilg(['gilg', '-a', 'rafael'])

        assert result['system'] == ["git log --author='rafael'"]

    def test_compare_option_resolves_branch(self, run_gilg):
        result = run_gilg(['gilg', '-c', 'dev'], compare_branch='develop')

        assert result['system'] == ['git log develop..']
        result['list_results'].find_branch_by_partial.assert_called_once_with('dev')

    def test_grep_option(self, run_gilg):
        result = run_gilg(['gilg', '-g', 'fix'])

        assert result['system'] == ["git log -i --grep='fix'"]

    def test_exclude_grep_option(self, run_gilg):
        result = run_gilg(['gilg', '-e', 'wip'])

        assert result['system'] == ["git log -i --grep='wip' --invert-grep"]

    def test_pretty_option(self, run_gilg):
        result = run_gilg(['gilg', '-p'])

        assert result['system'] == [f'git log {PRETTY_FLAG}']

    def test_stat_option(self, run_gilg):
        result = run_gilg(['gilg', '-s'])

        assert result['system'] == ['git log --stat']

    def test_diff_option(self, run_gilg):
        result = run_gilg(['gilg', '-d'])

        assert result['system'] == ['git log --patch-with-stat']

    def test_oneline_option(self, run_gilg):
        result = run_gilg(['gilg', '-o'])

        assert result['system'] == ['git log --oneline']

    def test_no_merges_option(self, run_gilg):
        result = run_gilg(['gilg', '-n'])

        assert result['system'] == ['git log --no-merges']

    def test_merges_option(self, run_gilg):
        result = run_gilg(['gilg', '-m'])

        assert result['system'] == ['git log --merges']

    def test_roadmap_option(self, run_gilg):
        result = run_gilg(['gilg', '-r'])

        assert result['system'] == ['git log --graph']

    def test_numeric_unmapped_option_becomes_target(self, run_gilg):
        result = run_gilg(['gilg', '-o', '-5'])

        assert result['system'] == ['git log --oneline -5']

    def test_combined_pretty_no_merges_graph_and_limit(self, run_gilg):
        result = run_gilg(['gilg', '-p', '-n', '-r', '-5'])

        assert result['system'] == [f'git log {PRETTY_FLAG} --no-merges --graph -5']


class TestBashGitLogEntryPoints:
    def test_go_instantiates_bash_git_log(self):
        with patch.object(BashGitLog, '__init__', return_value=None) as init_mock:
            BashGitLog.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitLog, 'go') as go_mock:
            gilg_main.run()

        go_mock.assert_called_once_with()
