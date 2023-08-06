# type: ignore
"""Test climates."""
from argparse import ArgumentParser
import pytest
from climates import Climate, microclimate


def test_microclimate(cmd_foo, cmd_bar, cmd_baz):
    """microclimate should insert subcommand into subparser."""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    microclimate(subparsers, "foo", cmd_foo)
    microclimate(subparsers, "bar", cmd_bar)
    microclimate(subparsers, "baz", cmd_baz)
    assert subparsers.choices["foo"].description == "Foo."
    assert subparsers.choices["bar"].description == "Bar."
    assert subparsers.choices["baz"].description == "Baz."


def test_climate():
    """Climate constructor must set description and empty commands."""
    cli = Climate("Test CLI app")
    assert cli.description == "Test CLI app"
    assert not cli.commands


def test_climate_add_commands(cli, cmd_foo, cmd_bar):
    """Climate.add_commands should add function to commands.

    It should use the function's name as key to Climate.commands.
    """
    cmd_baz = cmd_bar
    cli.add_commands(cmd_foo, cmd_baz)
    assert len(cli.commands) == 2
    assert cli.commands["foo"] == cmd_foo
    assert cli.commands["bar"] == cmd_bar


def test_climate_add_commands_with_kwargs(cli, cmd_foo, cmd_bar):
    """Climate.add_commands should add functions in kwargs to commands.

    But it should use the keys in kwargs instead of function.__name__.
    """
    cli.add_commands(cmd_foo, baz=cmd_bar)
    assert len(cli.commands) == 2
    assert cli.commands["foo"] == cmd_foo
    assert cli.commands["baz"] == cmd_bar


def test_climate_to_argparse(cli):
    """Climates.to_argparse should create an ArgumentParser object."""
    assert isinstance(cli.to_argparse(), ArgumentParser)


def test_climate_to_argparse_description():
    """Climates.to_argparse should get description from Climate.description."""
    cli = Climate("Test CLI app")
    parser = cli.to_argparse()
    assert cli.description == parser.description


def test_climate_to_argparse_with_commands(cli, cmd_foo, cmd_bar, cmd_baz):
    """Climates.to_argparse should not crash if there are commands."""
    cli.add_commands(cmd_foo, cmd_bar, cmd_baz)
    cli.to_argparse()


def test_climate_run(cli, cmd_foo, cmd_bar, cmd_baz):
    """Climate.run should invoke command handler specified in options."""
    cli.add_commands(cmd_foo, cmd_bar, cmd_baz)
    res_foo = cli.run(["foo", "1"])
    res_bar = cli.run(["bar", "1", "--b", "2", "3"])
    res_baz = cli.run(["baz", "1", "--b", "2", "3", "--c", "c:4", "d:5",
                       "e:6"])
    assert res_foo == ("foo", "1")
    assert res_bar == ("bar", "1", ("2", "3"))
    assert res_baz == ("baz", "1", ("2", "3"), dict(c="4", d="5", e="6"))


def test_climate_run_with_positional_only_parameters(cli):
    """Climate.run should add positional arguments to the subparser."""
    def func(foo, bar: int, baz="hello", /):
        """Test function."""
        return foo, bar, baz
    cli.add_commands(func)
    foo, bar, baz = cli.run(["func", "foo", "1", "baz"])
    assert foo == "foo"
    assert bar == 1
    assert baz == "baz"


def test_climate_run_with_keyword_only_parameters(cli):
    """Climate.run should add named arguments to the subparser. """
    def func(*, foo, bar: int, baz="hello"):
        """Test function."""
        return foo, bar, baz
    cli.add_commands(func)
    command = "func --foo foo --bar 1 --baz baz".split()
    foo, bar, baz = cli.run(command)
    assert foo == "foo"
    assert bar == 1
    assert baz == "baz"


def test_climate_run_with_required_keyword_only_parameter(cli):
    """Climate.run should abort if the argument isn't given."""
    def func(*, _arg):
        """Test function."""
    cli.add_commands(func)
    with pytest.raises(SystemExit):
        cli.run(["func"])


def test_climate_run_with_parameter_with_callable_annotation(cli):
    """Climate.run should automatically use it to convert values."""
    def func(arg: float):
        """Test function."""
        return arg
    cli.add_commands(func)
    result = cli.run(["func", "--arg", "1.5"])
    assert result == 1.5


def test_climate_run_with_var_positional_parameter(cli):
    """Climate.run should abort the program if there's an invalid argument.

    It should otherwise convert the values to the specified type.
    """
    def func(*args: int):
        """Test function."""
        return args
    cli.add_commands(func)
    with pytest.raises(SystemExit):
        cli.run(["func", "--args", "a"])

    result = cli.run(["func", "--args", "1", "2"])
    assert result == (1, 2)


def test_climate_run_with_var_keyword_parameter(cli):
    """Climate.run should abort the program if there's an invalid argument.

    Otherwise, it should convert the values to the specified type.
    """
    def func(**kwargs: int):
        """Test function."""
        return kwargs
    cli.add_commands(func)
    with pytest.raises(SystemExit):
        cli.run(["func", "--kwargs", "a1"])
    with pytest.raises(SystemExit):
        cli.run(["func", "--kwargs", "a:a"])
    result = cli.run(["func", "--kwargs", "a:1", "b:2"])
    assert result == {"a": 1, "b": 2}


def test_climate_run_with_multiple_values_for_argument(cli):
    """Climate.run should abort the program."""
    def func(arg="foo", **kwargs):
        """Test function."""
        return arg, kwargs
    cli.add_commands(func)
    with pytest.raises(SystemExit):
        cli.run(["func", "--kwargs", "arg:bar"])
