import pytest
from unittest.mock import patch

from gitbro.gibr.BashGitBranch import BashGitBranch
from gitbro.gibr import main as gibr_main


@pytest.fixture(autouse=True)
def reset_bash_git_branch_state():
    BashGitBranch.line = '{base} {action} {flags} {target}'
    BashGitBranch.base = 'git'
    BashGitBranch.action = 'branch'
    BashGitBranch.flags = []
    BashGitBranch.target = ''
    BashGitBranch.prompt = False
    BashGitBranch.question = ''
    yield
    BashGitBranch.line = '{base} {action} {flags} {target}'
    BashGitBranch.base = 'git'
    BashGitBranch.action = 'branch'
    BashGitBranch.flags = []
    BashGitBranch.target = ''
    BashGitBranch.prompt = False
    BashGitBranch.question = ''


@pytest.fixture
def run_gibr(monkeypatch):
    def _factory(argv, *, confirm='n', grep_branch='feature/foo', previous_branch='main'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('builtins.input', return_value=confirm) as input_mock, \
             patch(
                 'gitbro.gibr.BashGitBranch.ListResultsCaseIgnored'
             ) as list_results_mock:
            list_results_mock.return_value.find_branch_by_partial.return_value = grep_branch
            list_results_mock.return_value.find_last_branch_by_reflog.return_value = previous_branch

            instance = BashGitBranch()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'input_called': input_mock.called,
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitBranchListCommands:
    def test_no_arguments_lists_local_branches(self, run_gibr):
        result = run_gibr(['gibr'])

        assert result['printed'] == ['git branch -l']
        assert result['system'] == ['git branch -l']
        assert result['instance'].flags == ['-l']

    def test_list_option_lists_local_branches(self, run_gibr):
        result = run_gibr(['gibr', '-l'])

        assert result['system'] == ['git branch -l']

    def test_remotes_option_lists_remote_branches(self, run_gibr):
        result = run_gibr(['gibr', '-r'])

        assert result['system'] == ['git branch -r']

    def test_list_and_remotes_options_can_be_combined(self, run_gibr):
        result = run_gibr(['gibr', '-l', '-r'])

        assert result['system'] == ['git branch -l -r']


class TestBashGitBranchCheckoutCommands:
    def test_positional_branch_name_checks_out_branch(self, run_gibr):
        result = run_gibr(['gibr', 'my-branch'])

        assert result['system'] == ['git checkout my-branch']
        assert result['instance'].action == 'checkout'
        assert result['instance'].target == 'my-branch'

    def test_new_option_creates_and_checks_out_branch(self, run_gibr):
        result = run_gibr(['gibr', '-n', 'new-branch'])

        assert result['system'] == ['git checkout -b new-branch']
        assert result['instance'].flags == ['-b']
        assert result['instance'].target == 'new-branch'

    def test_previous_option_checks_out_previous_branch(self, run_gibr):
        result = run_gibr(['gibr', '-p'], previous_branch='develop')

        assert result['system'] == ['git checkout develop']
        result['list_results'].find_last_branch_by_reflog.assert_called_once_with()

    def test_grep_option_checks_out_matching_branch(self, run_gibr):
        result = run_gibr(['gibr', '-g', 'feat'], grep_branch='feature/login')

        assert result['system'] == ['git checkout feature/login']
        result['list_results'].find_branch_by_partial.assert_called_once_with('feat')


class TestBashGitBranchDeleteCommand:
    def test_delete_option_prompts_and_skips_when_not_confirmed(self, run_gibr):
        result = run_gibr(['gibr', '-d', 'old-branch'], confirm='n')

        assert result['input_called'] is True
        assert result['instance'].prompt is True
        assert result['instance'].question == (
            'Are you sure you want to delete the local old-branch? (Yy|Nn)'
        )
        assert result['printed'] == []
        assert result['system'] == []

    def test_delete_option_runs_when_confirmed_with_y(self, run_gibr):
        result = run_gibr(['gibr', '-d', 'old-branch'], confirm='y')

        assert result['system'] == ['git branch -d old-branch']

    def test_delete_option_runs_when_confirmed_with_Y(self, run_gibr):
        result = run_gibr(['gibr', '-d', 'old-branch'], confirm='Y')

        assert result['system'] == ['git branch -d old-branch']


class TestBashGitBranchEntryPoints:
    def test_go_instantiates_bash_git_branch(self):
        with patch.object(BashGitBranch, '__init__', return_value=None) as init_mock:
            BashGitBranch.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitBranch, 'go') as go_mock:
            gibr_main.run()

        go_mock.assert_called_once_with()
