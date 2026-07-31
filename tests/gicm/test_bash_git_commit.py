import pytest
from unittest.mock import patch

from gitbro.gicm.BashGitCommit import BashGitCommit
from gitbro.gicm import main as gicm_main


@pytest.fixture(autouse=True)
def reset_bash_git_commit_state():
    BashGitCommit.line = '{base} {action} {flags} {target}'
    BashGitCommit.base = 'git'
    BashGitCommit.action = 'commit'
    BashGitCommit.flags = []
    BashGitCommit.target = ''
    BashGitCommit.prompt = False
    BashGitCommit.question = 'Are you sure you want to reset the last commit? (Yy|Nn)'
    yield
    BashGitCommit.line = '{base} {action} {flags} {target}'
    BashGitCommit.base = 'git'
    BashGitCommit.action = 'commit'
    BashGitCommit.flags = []
    BashGitCommit.target = ''
    BashGitCommit.prompt = False
    BashGitCommit.question = 'Are you sure you want to reset the last commit? (Yy|Nn)'


@pytest.fixture
def run_gicm(monkeypatch):
    def _factory(argv, *, confirm='n'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('builtins.input', return_value=confirm) as input_mock:
            instance = BashGitCommit()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'input_called': input_mock.called,
            }

    return _factory


class TestBashGitCommitCommands:
    def test_no_arguments_runs_plain_commit(self, run_gicm):
        result = run_gicm(['gicm'])

        assert result['system'] == ['git commit']

    def test_positional_message(self, run_gicm):
        result = run_gicm(['gicm', 'fix', 'typo'])

        assert result['system'] == ["git commit -m 'fix typo'"]

    def test_message_option(self, run_gicm):
        result = run_gicm(['gicm', '-m', 'hello', 'world'])

        assert result['system'] == ["git commit -m 'hello world'"]

    def test_amend_defaults_to_no_edit(self, run_gicm):
        result = run_gicm(['gicm', '-a'])

        assert result['system'] == ['git commit --amend --no-edit']

    def test_amend_with_edit(self, run_gicm):
        result = run_gicm(['gicm', '-a', '-e'])

        assert result['system'] == ['git commit --amend --edit']

    def test_amend_with_ignore_message(self, run_gicm):
        result = run_gicm(['gicm', '-a', '-i'])

        assert result['system'] == ['git commit --amend --no-edit']

    def test_previous_message_option(self, run_gicm):
        result = run_gicm(['gicm', '-p'])

        assert result['system'] == ['git commit -c HEAD']

    def test_dry_run_and_no_verify(self, run_gicm):
        result = run_gicm(['gicm', '-d', '-n', '-m', 'msg'])

        assert result['system'] == ["git commit --dry-run --no-verify -m 'msg'"]

    def test_redo_resets_to_head_reflog(self, run_gicm):
        result = run_gicm(['gicm', '-r'])

        assert result['system'] == ['git reset HEAD@{1}']
        assert result['input_called'] is False

    def test_undo_prompts_and_skips_when_not_confirmed(self, run_gicm):
        result = run_gicm(['gicm', '-z'], confirm='n')

        assert result['input_called'] is True
        assert result['printed'] == []
        assert result['system'] == []

    def test_undo_runs_soft_reset_when_confirmed(self, run_gicm):
        result = run_gicm(['gicm', '-z'], confirm='y')

        assert result['system'] == ['git reset HEAD~1 --soft']


class TestBashGitCommitEntryPoints:
    def test_go_instantiates_bash_git_commit(self):
        with patch.object(BashGitCommit, '__init__', return_value=None) as init_mock:
            BashGitCommit.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitCommit, 'go') as go_mock:
            gicm_main.run()

        go_mock.assert_called_once_with()
