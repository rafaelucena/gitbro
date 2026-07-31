import pytest
from gitbro.abc.Arguments import Arguments

@pytest.fixture(autouse=True)
def reset_arguments_state():
    Arguments.options = []
    Arguments.values = []
    Arguments.matched = None
    yield
    Arguments.options = []
    Arguments.values = []
    Arguments.matched = None


@pytest.fixture
def arguments_from_argv(monkeypatch):
    def _factory(argv):
        monkeypatch.setattr('sys.argv', argv)
        return Arguments()

    return _factory


class TestArgumentsInit:
    def test_no_arguments_leaves_options_and_values_empty(self, arguments_from_argv):
        args = arguments_from_argv(['prog'])

        assert args.get_options() == []
        assert args.get_values() == []

    def test_classifies_dash_options_and_positional_values(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a', 'file.txt', '-b'])

        assert args.get_options() == ['-a', '-b']
        assert args.get_values() == ['file.txt']

    def test_numeric_options_are_inserted_at_the_front(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a', '-1', '-b', '-2'])

        assert args.get_options() == ['-2', '-1', '-a', '-b']
        assert args.get_values() == []

    def test_later_numeric_option_precedes_earlier_numeric_option(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-2', '-x', '-1'])

        assert args.get_options() == ['-1', '-2', '-x']

    def test_double_dash_argument_is_treated_as_value(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '--long', 'value'])

        assert args.get_options() == []
        assert args.get_values() == ['--long', 'value']

    def test_bare_dash_is_treated_as_value(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-', 'file.txt'])

        assert args.get_options() == []
        assert args.get_values() == ['-', 'file.txt']

    def test_argument_starting_with_digits_after_dash_is_numeric_option(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-12abc'])

        assert args.get_options() == ['-12abc']
        assert args.get_values() == []


class TestArgumentsAccessors:
    def test_get_option_returns_option_by_index(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a', '-b'])

        assert args.get_option() == '-a'
        assert args.get_option(0) == '-a'
        assert args.get_option(1) == '-b'

    def test_get_option_returns_empty_string_for_out_of_range_index(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a'])

        assert args.get_option(-1) == ''
        assert args.get_option(1) == ''
        assert args.get_option(99) == ''

    def test_get_option_returns_empty_string_when_no_options(self, arguments_from_argv):
        args = arguments_from_argv(['prog', 'value'])

        assert args.get_option() == ''

    def test_get_value_returns_value_by_index(self, arguments_from_argv):
        args = arguments_from_argv(['prog', 'first', 'second'])

        assert args.get_value() == 'first'
        assert args.get_value(0) == 'first'
        assert args.get_value(1) == 'second'

    def test_get_value_returns_empty_string_for_out_of_range_index(self, arguments_from_argv):
        args = arguments_from_argv(['prog', 'only'])

        assert args.get_value(-1) == ''
        assert args.get_value(1) == ''
        assert args.get_value(99) == ''

    def test_get_value_returns_empty_string_when_no_values(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a'])

        assert args.get_value() == ''

    def test_get_options_and_get_values_return_same_lists_as_attributes(self, arguments_from_argv):
        args = arguments_from_argv(['prog', '-a', 'file.txt'])

        assert args.get_options() is args.options
        assert args.get_values() is args.values

