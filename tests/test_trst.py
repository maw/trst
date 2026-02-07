import io
import sys

import pytest

from trst.cli import main


def run_trst(input_text, args):
    """Run trst with the given input and args, returning (stdout, stderr, exit_code)."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        sys.stdin = io.StringIO(input_text)
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        exit_code = main(args)
        return sys.stdout.getvalue(), sys.stderr.getvalue(), exit_code
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        sys.stderr = old_stderr


class TestBasicSubstitution:
    def test_simple_replacement(self):
        out, _, code = run_trst("hello world\n", ["hello", "goodbye"])
        assert out == "goodbye world\n"
        assert code == 0

    def test_regex_replacement(self):
        out, _, _ = run_trst("abc 123 def\n", ["[0-9]+", "NUM"])
        assert out == "abc NUM def\n"

    def test_multiple_search_terms_adjacent(self):
        out, _, _ = run_trst("helloworld\n", ["hello", "world", r"goodbye \2"])
        assert out == "goodbye world\n"

    def test_multiple_search_terms_with_spaces(self):
        out, _, _ = run_trst("hello world\n", ["-s", "hello", "world", r"goodbye \2"])
        assert out == "goodbye world\n"

    def test_no_match(self):
        out, _, code = run_trst("hello world\n", ["xyz", "abc"])
        assert out == "hello world\n"
        assert code == 0

    def test_empty_input(self):
        out, _, code = run_trst("", ["hello", "goodbye"])
        assert out == ""
        assert code == 0

    def test_multiple_lines(self):
        out, _, _ = run_trst("foo bar\nbaz foo\n", ["foo", "qux"])
        assert out == "qux bar\nbaz qux\n"


class TestLiteralMode:
    def test_literal_escapes_regex(self):
        out, _, _ = run_trst("a.b\n", ["-Q", "a.b", "x"])
        assert out == "x\n"

    def test_literal_does_not_match_regex(self):
        out, _, _ = run_trst("acb\n", ["-Q", "a.b", "x"])
        assert out == "acb\n"

    def test_literal_brackets(self):
        out, _, _ = run_trst("foo[0]\n", ["-Q", "[0]", "(zero)"])
        assert out == "foo(zero)\n"


class TestEscapePrefix:
    def test_default_percent_escape(self):
        out, _, _ = run_trst("a.b\n", ["%a.b", "x"])
        assert out == "x\n"

    def test_percent_no_regex_match(self):
        out, _, _ = run_trst("acb\n", ["%a.b", "x"])
        assert out == "acb\n"

    def test_custom_escape_char(self):
        out, _, _ = run_trst("a.b\n", ["-e", "@", "@a.b", "x"])
        assert out == "x\n"

    def test_unescaped_is_regex(self):
        out, _, _ = run_trst("acb\n", ["a.b", "x"])
        assert out == "x\n"


class TestSpacesFlag:
    def test_spaces_between_terms(self):
        out, _, _ = run_trst("hello world\n", ["-s", "hello", "world", r"\1 \2"])
        assert out == "hello world\n"

    def test_flexible_whitespace(self):
        out, _, _ = run_trst("hello    world\n", ["-s", "hello", "world", r"\1 \2"])
        assert out == "hello world\n"

    def test_no_spaces_flag_requires_adjacent(self):
        out, _, _ = run_trst("helloworld\n", ["hello", "world", r"\1-\2"])
        assert out == "hello-world\n"


class TestIgnoreCase:
    def test_case_insensitive_match(self):
        out, _, _ = run_trst("Hello World\n", ["-i", "hello", "goodbye"])
        assert out == "goodbye World\n"

    def test_case_insensitive_with_regex(self):
        out, _, _ = run_trst("FOO bar\n", ["-i", "foo", "baz"])
        assert out == "baz bar\n"


class TestDebugMode:
    def test_debug_shows_match(self):
        out, _, _ = run_trst("hello world\n", ["-d", "hello", "world", "replacement"])
        assert "matches" in out
        assert ">" in out
        assert "^" in out

    def test_debug_shows_no_match(self):
        out, _, _ = run_trst("hello world\n", ["-d", "xyz", "replacement"])
        assert "does not match" in out


class TestVerbose:
    def test_verbose_writes_to_stderr(self):
        _, err, _ = run_trst("hello\n", ["-v", "hello", "goodbye"])
        assert len(err) > 0


class TestBackreferences:
    def test_capture_group_backreference(self):
        out, _, _ = run_trst("helloworld\n", ["hello", "world", r"\2 \1"])
        assert out == "world hello\n"

    def test_backreference_with_spaces(self):
        out, _, _ = run_trst("hello world\n", ["-s", "hello", "world", r"\2 \1"])
        assert out == "world hello\n"

    def test_single_group_with_nested_captures(self):
        # trst wraps each search expr in (), so (a)(b)(c) becomes ((a)(b)(c))
        # \1 = whole match, \2=a, \3=b, \4=c
        out, _, _ = run_trst("abc\n", ["(a)(b)(c)", r"\4\3\2"])
        assert out == "cba\n"


class TestEdgeCases:
    def test_too_few_args(self):
        with pytest.raises(SystemExit):
            run_trst("hello\n", ["hello"])

    def test_no_args(self):
        with pytest.raises(SystemExit):
            run_trst("hello\n", [])

    def test_return_code_is_zero(self):
        _, _, code = run_trst("hello\n", ["hello", "goodbye"])
        assert code == 0
