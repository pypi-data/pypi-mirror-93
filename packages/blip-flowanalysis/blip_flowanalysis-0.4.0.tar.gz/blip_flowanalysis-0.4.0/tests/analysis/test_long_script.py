import typing as tp
import itertools as it

import pytest
from pytest_mock import MockFixture

from blip_flowanalysis.analysis.long_script import JavaScriptEvaluator

class TestJavaScriptEvaluator(object):
    
    @pytest.fixture
    def evaluator(self) -> JavaScriptEvaluator:
        return JavaScriptEvaluator()
    
    @pytest.mark.parametrize('script_expected', [
        ('content', 'content'),
        ('content: "a // b"', 'content: "a // b"'),
        ('content: "x /* y */"', 'content: "x /* y */"'),
    ])
    def test_remove_comments_has_no_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content // comment', 'content '),
        ('// comment\n content', '\n content'),
        ('// comment1\n// comment2\ncontent', '\n\ncontent'),
    ])
    def test_remove_comments_has_one_line_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content /* comment */', 'content '),
        ('/* comment\ncomment */\n content', '\n content'),
        ('/* comment\ncomment */\n/* comment */\n content', '\n\n content'),
    ])
    def test_remove_comments_has_multi_lines_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content', 'content'),
    ])
    def test_hide_strings_has_no_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ("content 'string'", 'content --------'),
        ("content 'string1''string2'!", 'content ------------------!'),
        ("content 'string\nstring'", 'content ---------------'),
    ])
    def test_hide_strings_has_single_quoted_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content "string"', 'content --------'),
        ('content "string1""string2"!', 'content ------------------!'),
        ('content "string\nstring"', 'content ---------------'),
    ])
    def test_hide_strings_has_double_quoted_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no scope', (-1, -1)),
    ])
    def test_find_scope_has_no_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('ignore (scope)', (7, 13)),
        ('(scope1) (scope2)', (0, 7)),
    ])
    def test_find_scope_has_single_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('ignore (scope (inside))', (7, 22)),
        ('(scope (a) b (c) d)', (0, 18)),
        ('K * (a * (1 + (x - 1) / d) - 10)', (4, 31)),
    ])
    def test_find_scope_has_multi_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no function', []),
    ])
    def test_list_functions_has_no_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
                'function my_func(): {a = 1; print(a);}',
                ['a = 1; print(a);']
        ),
        (
                'function my_func():\n{\n  a = 1;\n  print(a);\n}',
                ['\n  a = 1;\n  print(a);\n']
        ),
        (
                'const func_1 = (a) =>\n{\n  print(a);\n}\n\n'
                'function func_2 (x):\n{\n  return x*x;\n}',
                ['\n  print(a);\n', '\n  return x*x;\n']
        ),
    ])
    def test_list_functions_has_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
                'function my_func():'
                '\n{'
                '\n  a = 1;'
                '\n  function show(x):'
                '\n  {'
                '\n    print(x + a);'
                '\n  }'
                '\n}',
                ['\n  a = 1;'
                 '\n  function show(x):'
                 '\n  {'
                 '\n    print(x + a);'
                 '\n  }'
                 '\n']
        ),
    ])
    def test_list_functions_has_functions_inside_of_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no excess spaces', 'no excess spaces'),
    ])
    def test_remove_excess_spaces_has_no_excess_spaces(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_excess_spaces(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('  excess on the left', 'excess on the left'),
        ('excess on the right  ', 'excess on the right'),
        ('excess   inside', 'excess inside'),
        ('excess \t  with\ttab', 'excess with tab'),
        ('excess   at   \n  multi  lines', 'excess at\nmulti lines'),
    ])
    def test_remove_excess_spaces_has_excess_spaces(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_excess_spaces(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there is no multi line', 'there is no multi line'),
    ])
    def test_remove_new_lines_has_no_new_lines(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]):
        script, expected = script_expected
        result = evaluator._remove_new_lines(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there is\nmulti line', 'there is multi line'),
        ('there is\n  more \n multi line', 'there is   more   multi line'),
    ])
    def test_remove_new_lines_has_new_lines(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]):
        script, expected = script_expected
        result = evaluator._remove_new_lines(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
            'var x = 1;'
            '\nvar y = "var x = 1; if (x == 1) {}...";'
            '\nprint("coffee");',
            [
                'var x = 1;',
                'var y = "var x = 1; if (x == 1) {}...";',
                'print("coffee");',
            ]
        ),
        (
            'var x = 1;'
            '\nif (x == 1) {'
            '\n  print("coffee");'
            '\n}'
            '\nelse {'
            '\n  print("tea");'
            '\n}',
            [
                'var x = 1;',
                'if (x == 1)',
                'print("coffee");',
                'print("tea");',
            ]
        )
    ])
    def test_split_commands_simple_scripts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._split_commands(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no numbers', 'there are no numbers'),
        ('do not remove1234567890', 'do not remove1234567890'),
    ])
    def test_remove_numbers_has_no_numbers(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_numbers(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this 1234567890', 'remove this '),
        ('var x = 2 + 2;', 'var x =  + ;'),
        ('var x = 2.1;', 'var x = ;'),
        ('var x = -2;', 'var x = ;'),
        ('var x = -2.1;', 'var x = ;'),
    ])
    def test_remove_numbers_has_numbers(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_numbers(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no strings', 'there are no strings'),
    ])
    def test_remove_strings_has_no_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this "1234567890"', 'remove this '),
        ("var x = '2' + '2';", "var x =  + ;")
    ])
    def test_remove_strings_has_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no lists', 'there are no lists'),
    ])
    def test_remove_lists_has_no_lists(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_lists(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this: [1234567890, "1234567890"]', 'remove this: '),
        ("var x = [2, '2'];", "var x = ;")
    ])
    def test_remove_lists_has_lists(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_lists(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no dicts', 'there are no dicts'),
    ])
    def test_remove_dicts_has_no_dicts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_dicts(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this: {"a": 123, "b": "123"}', 'remove this: '),
        ("var x = {'a': 2, 'b': '2'};", "var x = ;")
    ])
    def test_remove_dicts_has_dicts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_dicts(script)
        assert result == expected
    
    def test_remove_static_values(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        str_mock = mocker.Mock(spec=str)
        
        remove_dicts = mocker.Mock(return_value=str_mock)
        remove_lists = mocker.Mock(return_value=str_mock)
        remove_strings = mocker.Mock(return_value=str_mock)
        remove_numbers = mocker.Mock(return_value=str_mock)
        
        evaluator._remove_dicts = remove_dicts
        evaluator._remove_lists = remove_lists
        evaluator._remove_strings = remove_strings
        evaluator._remove_numbers = remove_numbers
        
        script = str_mock
        expected = str_mock
        result = evaluator._remove_static_values(script)
        assert result is expected
        
        remove_numbers.assert_called_once_with(str_mock)
        remove_strings.assert_called_once_with(str_mock)
        remove_lists.assert_called_once_with(str_mock)
        remove_dicts.assert_called_once_with(str_mock)
    
    @pytest.mark.parametrize('script_expected', [
        (
            '/* This is a comment. */'
            'function run(a, b, c) {'
            '  if (a > 0) {'
            '    var type = "up";'
            '  }'
            '  else {'
            '    var type = "down";'
            '  }'
            '  print("type", type);'
            '  for (var x = 0; x < 10; x ++) {'
            '    var y =     quadratic(x);'
            '    print(x, y);'
            '  }'
            '  return 1;'
            '}'
            ''
            'function quadratic(a, b, c, x) {'
            '  return a * x * x + b * x + c;'
            '}',
            143
        )
    ])
    def test_count_chars_simple_scripts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, int]) -> None:
        script, expected = script_expected
        result = evaluator.count_chars(script)
        assert result == expected
    
    def test_count_chars_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_commands = 12
        n_functions = 3
        n_chars_command = 10
        str_mock = mocker.MagicMock(spec=str)
        list_commands = list(it.repeat(str_mock, n_commands))
        list_functions = list(it.repeat(str_mock, n_functions))
        
        str_mock_len = mocker.Mock(return_value=n_chars_command)
        split_commands = mocker.Mock(return_value=list_commands)
        remove_excess_spaces = mocker.Mock(return_value=str_mock)
        remove_new_lines = mocker.Mock(return_value=str_mock)
        list_functions = mocker.Mock(return_value=list_functions)
        remove_static_values = mocker.Mock(return_value=str_mock)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        str_mock.__len__ = str_mock_len
        evaluator._split_commands = split_commands
        evaluator._remove_excess_spaces = remove_excess_spaces
        evaluator._remove_new_lines = remove_new_lines
        evaluator._list_functions = list_functions
        evaluator._remove_static_values = remove_static_values
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 360
        result = evaluator.count_chars(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        remove_static_values.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
        remove_excess_spaces.assert_called_once_with(str_mock)
        remove_new_lines.assert_called_once_with(str_mock)
        split_commands.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions)))
        str_mock_len.assert_has_calls(list(it.repeat(
            mocker.call(), n_functions * n_commands)))
    
    def test_count_lines_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_empty_lines = 9
        n_filled_lines = 3
        str_mock = mocker.MagicMock(spec=str)
        str_mock_empty = mocker.MagicMock(spec=str)
        list_lines =\
            list(it.repeat(str_mock, n_filled_lines))\
            + list(it.repeat(str_mock_empty, n_empty_lines))
        
        str_strip = mocker.Mock(return_value='a')
        str_strip_empty = mocker.Mock(return_value='')
        str_mock_splitlines = mocker.Mock(return_value=list_lines)
        remove_static_values = mocker.Mock(return_value=str_mock)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        str_mock.strip = str_strip
        str_mock_empty.strip = str_strip_empty
        str_mock.splitlines = str_mock_splitlines
        evaluator._remove_static_values = remove_static_values
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 3
        result = evaluator.count_lines(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        remove_static_values.assert_called_once_with(str_mock)
        str_mock_splitlines.assert_called_once_with()
        str_strip.assert_has_calls(list(it.repeat(
            mocker.call(), n_filled_lines)))
        str_strip_empty.assert_has_calls(list(it.repeat(
            mocker.call(), n_empty_lines)))
    
    def test_count_functions_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_functions = 3
        str_mock = mocker.MagicMock(spec=str)
        list_functions = list(it.repeat(str_mock, n_functions))
        
        remove_new_lines = mocker.Mock(return_value=str_mock)
        list_functions = mocker.Mock(return_value=list_functions)
        remove_excess_spaces = mocker.Mock(return_value=str_mock)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        evaluator._remove_new_lines = remove_new_lines
        evaluator._list_functions = list_functions
        evaluator._remove_excess_spaces = remove_excess_spaces
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 3
        result = evaluator.count_functions(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        remove_excess_spaces.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
        remove_new_lines.assert_called_once_with(str_mock)
    
    def test_count_commands_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_commands = 12
        n_functions = 3
        str_mock = mocker.MagicMock(spec=str)
        list_commands = list(it.repeat(str_mock, n_commands))
        list_functions = list(it.repeat(str_mock, n_functions))
        
        split_commands = mocker.Mock(return_value=list_commands)
        remove_excess_spaces = mocker.Mock(return_value=str_mock)
        remove_new_lines = mocker.Mock(return_value=str_mock)
        list_functions = mocker.Mock(return_value=list_functions)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        evaluator._split_commands = split_commands
        evaluator._remove_excess_spaces = remove_excess_spaces
        evaluator._remove_new_lines = remove_new_lines
        evaluator._list_functions = list_functions
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 36
        result = evaluator.count_commands(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
        remove_excess_spaces.assert_called_once_with(str_mock)
        remove_new_lines.assert_called_once_with(str_mock)
        split_commands.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions)))
