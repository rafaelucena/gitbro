import pytest
from unittest.mock import patch

from gitbro.gibk.BashGitStash import BashGitStash
from gitbro.gibk import main as gibk_main


LIST_FLAGS = 'list --pretty=format:"%gd: %C(green)(%cr)%C(reset): %s"'


@pytest.fixture(autouse=True)
def reset_bash_git_stash_state():
    BashGitStash.line = '{base} {action} {flags} {target} {comment}'
    BashGitStash.base = 'git'
    BashGitStash.action = 'stash'
    BashGitStash.flags = []
    BashGitStash.target = ''
    BashGitStash.comment = ''
    BashGitStash.prompt = False
    BashGitStash.question = ''
    yield
    BashGitStash.line = '{base} {action} {flags} {target} {comment}'
    BashGitStash.base = 'git'
    BashGitStash.action = 'stash'
    BashGitStash.flags = []
    BashGitStash.target = ''
    BashGitStash.comment = ''
    BashGitStash.prompt = False
    BashGitStash.question = ''


@pytest.fixture
def run_gibk(monkeypatch):
    def _factory(argv, *, confirm='y', stash_item=None):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('builtins.input', return_value=confirm) as input_mock, \
             patch('gitbro.gibk.BashGitStash.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_stash_list_grouped.return_value = stash_item

            instance = BashGitStash()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'input_called': input_mock.called,
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitStashCommands:
    def test_no_arguments_lists_stashes(self, run_gibk):
        result = run_gibk(['gibk'])

        assert result['system'] == [f'git stash {LIST_FLAGS}']

    def test_list_option(self, run_gibk):
        result = run_gibk(['gibk', '-l'])

        assert result['system'] == [f'git stash {LIST_FLAGS}']

    def test_new_without_message(self, run_gibk):
        result = run_gibk(['gibk', '-n'])

        assert result['system'] == ['git stash push']

    def test_new_with_message(self, run_gibk):
        result = run_gibk(['gibk', '-n', 'wip'])

        assert result['system'] == ['git stash push -m wip']

    def test_clear_skips_when_not_confirmed(self, run_gibk):
        result = run_gibk(['gibk', '-c'], confirm='n')

        assert result['input_called'] is True
        assert result['printed'] == []
        assert result['system'] == []

    def test_clear_runs_when_confirmed(self, run_gibk):
        result = run_gibk(['gibk', '-c'], confirm='y')

        assert result['system'] == ['git stash clear']

    def test_drop_without_index(self, run_gibk):
        result = run_gibk(['gibk', '-d'], confirm='y')

        assert result['system'] == ['git stash drop']

    def test_drop_with_index(self, run_gibk):
        result = run_gibk(['gibk', '-d', '2'], confirm='Y')

        assert result['system'] == ['git stash drop stash@{2}']

    def test_show_option(self, run_gibk):
        result = run_gibk(['gibk', '-s'])

        assert result['system'] == ['git stash show']

    def test_show_with_index(self, run_gibk):
        result = run_gibk(['gibk', '-s', '1'])

        assert result['system'] == ['git stash show stash@{1}']

    def test_view_option_adds_patch(self, run_gibk):
        result = run_gibk(['gibk', '-v'])

        assert result['system'] == ['git stash show -p']

    def test_view_with_index(self, run_gibk):
        result = run_gibk(['gibk', '-v', '3'])

        assert result['system'] == ['git stash show -p stash@{3}']

    def test_apply_option(self, run_gibk):
        result = run_gibk(['gibk', '-a'])

        assert result['system'] == ['git stash apply']

    def test_apply_with_index(self, run_gibk):
        result = run_gibk(['gibk', '-a', '1'])

        assert result['system'] == ['git stash apply stash@{1}']

    def test_pop_option(self, run_gibk):
        result = run_gibk(['gibk', '-p'])

        assert result['system'] == ['git stash pop']

    def test_pop_with_index(self, run_gibk):
        result = run_gibk(['gibk', '-p', '0'])

        assert result['system'] == ['git stash pop stash@{0}']

    def test_positional_index_shows_stash(self, run_gibk):
        result = run_gibk(['gibk', '4'])

        assert result['system'] == ['git stash show stash@{4}']

    def test_grep_hit_sets_target_and_comment(self, run_gibk):
        stash_item = {
            'stash': 'stash@{2}',
            'branch': 'feature',
            'message': 'wip login',
        }
        result = run_gibk(['gibk', '-g', 'login'], stash_item=stash_item)

        assert result['system'] == ['git stash show stash@{2} #feature: wip login']
        result['list_results'].find_stash_list_grouped.assert_called_once_with('login')

    def test_grep_miss_falls_back_to_negative_index(self, run_gibk):
        result = run_gibk(['gibk', '-g', 'missing'], stash_item=None)

        assert result['system'] == ['git stash show stash@{-1}']


class TestBashGitStashEntryPoints:
    def test_go_instantiates_bash_git_stash(self):
        with patch.object(BashGitStash, '__init__', return_value=None) as init_mock:
            BashGitStash.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitStash, 'go') as go_mock:
            gibk_main.run()

        go_mock.assert_called_once_with()
