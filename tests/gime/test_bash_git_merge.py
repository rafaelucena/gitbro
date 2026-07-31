import pytest
from unittest.mock import patch

from gitbro.gime.BashGitMerge import BashGitMerge
from gitbro.gime import main as gime_main


@pytest.fixture(autouse=True)
def reset_bash_git_merge_state():
    BashGitMerge.line = '{base} {action} {flags} {target}'
    BashGitMerge.base = 'git'
    BashGitMerge.action = 'merge'
    BashGitMerge.flags = []
    BashGitMerge.target = ''
    BashGitMerge.prompt = False
    BashGitMerge.question = ''
    yield
    BashGitMerge.line = '{base} {action} {flags} {target}'
    BashGitMerge.base = 'git'
    BashGitMerge.action = 'merge'
    BashGitMerge.flags = []
    BashGitMerge.target = ''
    BashGitMerge.prompt = False
    BashGitMerge.question = ''


@pytest.fixture
def run_gime(monkeypatch):
    def _factory(argv, *, confirm='y', grep_branch='feature/foo', previous_branch='develop'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('builtins.input', return_value=confirm) as input_mock, \
             patch('gitbro.gime.BashGitMerge.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_branch_by_partial.return_value = grep_branch
            list_results_mock.return_value.find_last_branch_by_reflog.return_value = previous_branch

            instance = BashGitMerge()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'input_called': input_mock.called,
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitMergeCommands:
    def test_no_arguments_runs_plain_merge(self, run_gime):
        result = run_gime(['gime'])

        assert result['system'] == ['git merge']
        assert result['input_called'] is False

    def test_positional_branch_merges_without_prompt(self, run_gime):
        result = run_gime(['gime', 'feat'], grep_branch='feature/login')

        assert result['system'] == ['git merge feature/login']
        assert result['input_called'] is False
        result['list_results'].find_branch_by_partial.assert_called_once_with('feat')

    def test_abort_option(self, run_gime):
        result = run_gime(['gime', '-a'])

        assert result['system'] == ['git merge --abort']

    def test_continue_option(self, run_gime):
        result = run_gime(['gime', '-c'])

        assert result['system'] == ['git merge --continue']

    def test_quit_option(self, run_gime):
        result = run_gime(['gime', '-q'])

        assert result['system'] == ['git merge --quit']

    def test_previous_option_prompts_and_merges(self, run_gime):
        result = run_gime(['gime', '-p'], confirm='y', previous_branch='develop')

        assert result['input_called'] is True
        assert result['instance'].question == (
            'Are you sure you want to merge the branch (develop) into this one? (Yy|Nn)'
        )
        assert result['system'] == ['git merge develop']

    def test_grep_option_prompts_and_merges(self, run_gime):
        result = run_gime(['gime', '-g', 'feat'], confirm='Y', grep_branch='feature/foo')

        assert result['system'] == ['git merge feature/foo']
        result['list_results'].find_branch_by_partial.assert_called_with('feat')

    def test_master_option_prompts_and_merges(self, run_gime):
        result = run_gime(['gime', '-m'], confirm='y')

        assert result['system'] == ['git merge master']

    def test_prompted_merge_skips_when_not_confirmed(self, run_gime):
        result = run_gime(['gime', '-m'], confirm='n')

        assert result['printed'] == []
        assert result['system'] == []

    def test_ignore_edit_stat_dry_run_and_no_verify_flags(self, run_gime):
        result = run_gime(['gime', '-m', '-i', '-s', '-d', '-n'], confirm='y')

        assert result['system'] == [
            'git merge --no-edit --stat --no-commit --no-ff --no-verify master'
        ]

    def test_edit_flag(self, run_gime):
        result = run_gime(['gime', '-m', '-e'], confirm='y')

        assert result['system'] == ['git merge --edit master']


class TestBashGitMergeEntryPoints:
    def test_go_instantiates_bash_git_merge(self):
        with patch.object(BashGitMerge, '__init__', return_value=None) as init_mock:
            BashGitMerge.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitMerge, 'go') as go_mock:
            gime_main.run()

        go_mock.assert_called_once_with()
