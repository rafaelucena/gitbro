import pytest
from unittest.mock import patch

from gitbro.gipx.BashGitPush import BashGitPush
from gitbro.gipx import main as gipx_main


NO_UPSTREAM_OUTPUT = (
    "fatal: The current branch feature has no upstream branch.\n"
    "To push the current branch and set the remote as upstream, use\n"
    "\n"
    "    git push --set-upstream origin feature\n"
)


@pytest.fixture(autouse=True)
def reset_bash_git_push_state():
    BashGitPush.line = '{base} {action} {flags} {target}'
    BashGitPush.base = 'git'
    BashGitPush.action = 'push'
    BashGitPush.flags = []
    BashGitPush.target = ''
    BashGitPush.prompt = False
    BashGitPush.question = ''
    BashGitPush.tried_output = ''
    BashGitPush.suggested_command = ''
    yield
    BashGitPush.line = '{base} {action} {flags} {target}'
    BashGitPush.base = 'git'
    BashGitPush.action = 'push'
    BashGitPush.flags = []
    BashGitPush.target = ''
    BashGitPush.prompt = False
    BashGitPush.question = ''
    BashGitPush.tried_output = ''
    BashGitPush.suggested_command = ''


@pytest.fixture
def run_gipx(monkeypatch):
    def _factory(argv, *, confirm='n', push_output='Everything up-to-date', head_branch='feature'):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('builtins.input', return_value=confirm) as input_mock, \
             patch('subprocess.getoutput') as getoutput_mock:
            def _getoutput(command):
                if command == 'git rev-parse --abbrev-ref HEAD':
                    return head_branch
                return push_output

            getoutput_mock.side_effect = _getoutput

            instance = BashGitPush()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'input_called': input_mock.called,
                'getoutput_calls': [call.args[0] for call in getoutput_mock.call_args_list],
            }

    return _factory


class TestBashGitPushCommands:
    def test_no_arguments_runs_plain_push(self, run_gipx):
        result = run_gipx(['gipx'])

        assert result['printed'][0] == 'git push'
        assert 'git push' in result['getoutput_calls']
        assert result['system'] == []

    def test_no_verify_option(self, run_gipx):
        result = run_gipx(['gipx', '-n'])

        assert result['printed'][0] == 'git push --no-verify'
        assert 'git push --no-verify' in result['getoutput_calls']

    def test_set_upstream_with_explicit_branch(self, run_gipx):
        result = run_gipx(['gipx', '-u', 'custom-branch'])

        assert result['printed'][0] == 'git push --set-upstream origin custom-branch'

    def test_set_upstream_without_name_uses_current_branch(self, run_gipx):
        result = run_gipx(['gipx', '-u'], head_branch='feature')

        assert result['printed'][0] == 'git push --set-upstream origin feature'
        assert 'git rev-parse --abbrev-ref HEAD' in result['getoutput_calls']

    def test_force_option_skips_when_not_confirmed(self, run_gipx):
        result = run_gipx(['gipx', '-f'], confirm='n')

        assert result['input_called'] is True
        assert result['printed'] == []
        assert result['getoutput_calls'] == []
        assert result['system'] == []

    def test_force_option_runs_when_confirmed(self, run_gipx):
        result = run_gipx(['gipx', '-f'], confirm='y')

        assert result['printed'][0] == 'git push --force'
        assert 'git push --force' in result['getoutput_calls']

    def test_missing_upstream_offers_suggested_command_and_runs_on_confirm(self, run_gipx):
        result = run_gipx(['gipx'], confirm='y', push_output=NO_UPSTREAM_OUTPUT)

        assert result['instance'].suggested_command == 'git push --set-upstream origin feature'
        assert 'git push --set-upstream origin feature' in result['printed']
        assert result['system'] == ['git push --set-upstream origin feature']

    def test_missing_upstream_skips_suggested_command_when_declined(self, run_gipx):
        result = run_gipx(['gipx'], confirm='n', push_output=NO_UPSTREAM_OUTPUT)

        assert result['system'] == []
        assert result['instance'].suggested_command == 'git push --set-upstream origin feature'


class TestBashGitPushEntryPoints:
    def test_go_instantiates_bash_git_push(self):
        with patch.object(BashGitPush, '__init__', return_value=None) as init_mock:
            BashGitPush.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitPush, 'go') as go_mock:
            gipx_main.run()

        go_mock.assert_called_once_with()
