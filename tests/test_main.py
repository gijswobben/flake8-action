import click
import pytest

from main import _parse_input_list


@pytest.mark.parametrize("content", ["A,E501,B", "A,E501 ,B", "A  ,E501,B"])
def test__parse_input_list(content: str):
    result = _parse_input_list(
        context=click.Context(click.Command("test")),
        param=click.Option(["--test"]),
        content=content,
    )
    assert result == ["A", "E501", "B"]
