import pytest
from unittest.mock import patch

from gitbro.giad.BashGitAdd import BashGitAdd
from gitbro.giad import main as giad_main


@pytest.fixture(autouse=True)
def reset_bash_git_add_state():
    BashGitAdd.line = '{base} {action} {flags} {target}'
    BashGitAdd.base = 'git'
    BashGitAdd.action = 'add'
    BashGitAdd.flags = []
    BashGitAdd.target = ''
    yield
    BashGitAdd.line = '{base} {action} {flags} {target}'
    BashGitAdd.base = 'git'
    BashGitAdd.action = 'add'
    BashGitAdd.flags = []
    BashGitAdd.target = ''


@pytest.fixture
def run_giad(monkeypatch):
    def _factory(
        argv,
        *,
        changed='src/file.py',
        untracked_files='src/new.py',
        untracked_file='src/new.py',
    ):
        monkeypatch.setattr('sys.argv', argv)

        with patch('os.system') as system_mock, \
             patch('builtins.print') as print_mock, \
             patch('gitbro.giad.BashGitAdd.ListResultsCaseIgnored') as list_results_mock:
            list_results_mock.return_value.find_changed_files_for_diff.return_value = changed
            list_results_mock.return_value.find_untracked_files_for_add.return_value = untracked_files
            list_results_mock.return_value.find_untracked_file_for_add.return_value = untracked_file

            instance = BashGitAdd()

            return {
                'instance': instance,
                'printed': [call.args[0] for call in print_mock.call_args_list],
                'system': [call.args[0] for call in system_mock.call_args_list],
                'list_results': list_results_mock.return_value,
            }

    return _factory


class TestBashGitAddCommands:
    def test_no_arguments_runs_plain_add(self, run_giad):
        result = run_giad(['giad'])

        assert result['system'] == ['git add']

    def test_all_option(self, run_giad):
        result = run_giad(['giad', '-a'])

        assert result['system'] == ['git add --all']

    def test_modified_option(self, run_giad):
        result = run_giad(['giad', '-m'])

        assert result['system'] == ['git add -u']

    def test_update_option(self, run_giad):
        result = run_giad(['giad', '-u'])

        assert result['system'] == ['git add -u']

    def test_new_option_adds_exact_untracked_file(self, run_giad):
        result = run_giad(['giad', '-n', 'new'], untracked_file='src/new.py')

        assert result['system'] == ['git add src/new.py']
        result['list_results'].find_untracked_file_for_add.assert_called_once_with('new')

    def test_intent_option_adds_untracked_match_with_wildcards(self, run_giad):
        result = run_giad(['giad', '-i', 'new'], untracked_files='src/new.py')

        assert result['system'] == ['git add --intent-to-add *src/new.py*']
        result['list_results'].find_untracked_files_for_add.assert_called_once_with('new')

    def test_intent_option_with_short_extension_suffix_wildcard(self, run_giad):
        result = run_giad(['giad', '-i', 'new'], untracked_files='src/new.c')

        assert result['system'] == ['git add --intent-to-add *src/new.c']

    def test_positional_uses_changed_file_with_wildcards(self, run_giad):
        result = run_giad(['giad', 'file'], changed='src/file.py')

        assert result['system'] == ['git add *src/file.py*']
        result['list_results'].find_changed_files_for_diff.assert_called_once_with('file')

    def test_positional_falls_back_to_untracked_when_unchanged(self, run_giad):
        result = run_giad(
            ['giad', 'file'],
            changed='file',
            untracked_files='src/newfile',
        )

        assert result['system'] == ['git add *src/newfile*']
        result['list_results'].find_untracked_files_for_add.assert_called_once_with('file')

    def test_positional_with_short_extension_suffix_wildcard(self, run_giad):
        result = run_giad(['giad', 'file'], changed='src/file.c')

        assert result['system'] == ['git add *src/file.c']


class TestBashGitAddEntryPoints:
    def test_go_instantiates_bash_git_add(self):
        with patch.object(BashGitAdd, '__init__', return_value=None) as init_mock:
            BashGitAdd.go()

        init_mock.assert_called_once_with()

    def test_main_run_delegates_to_go(self):
        with patch.object(BashGitAdd, 'go') as go_mock:
            giad_main.run()

        go_mock.assert_called_once_with()
