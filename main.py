from __future__ import annotations

import re
from enum import Enum
from pathlib import Path

import click

flake8_result_pattern = re.compile(
    (
        r"(?P<file>.+):(?P<line>\d+):(?P<col>\d+):"
        r" (?P<code>[A-Z]+\d+)\s(?P<message>.+)"
    )
)
message_template = (
    "::{level} file={file},line={line},col={col},"
    "title={message_title}::{code} - {message}"
)


class Flake8ActionException(Exception):
    ...


class MessageLevel(Enum):
    DEBUG = "debug"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"


def _parse_input_list(
    context: click.Context, param: click.Parameter, content: str
) -> list[str]:
    """Parse comma separated input into a list of strings.

    Args:
        context (click.Context): The CLI context.
        param (click.Parameter): The parameter that is being parsed.
        content (str): The input content.

    Returns:
        list[str]: The result as a list of strings.
    """
    return [element.strip() for element in content.split(",") if element.strip() != ""]


@click.command()
@click.option("--strict", type=click.BOOL, default=False)
@click.option("--strict-for", callback=_parse_input_list, default="")
@click.option("--not-strict-for", callback=_parse_input_list, default="")
@click.option("--message-title", default="Flake8 issue found")
@click.option("--flake8-output", default=None)
def main(
    strict: bool,
    strict_for: list[str],
    not_strict_for: list[str],
    message_title: str,
    flake8_output: str | None,
) -> None:

    # Read the Flake8 results
    if flake8_output is None:
        flake8_output_path = Path("flake8_results.txt")
        flake8_lines = flake8_output_path.read_text().splitlines()
    else:
        flake8_lines = flake8_output.splitlines(keepends=False)

    # Keep track of whether or not this pipeline job should raise an
    # Exception (break the pipeline)
    should_raise = False

    # Make a list of outputs for this job
    output_lines: dict[str, list[str]] = {"warning": [], "error": []}

    # Go over every result in the Flake8 results and print a warning if
    # the file/line combination changed in this branch
    for flake8_line in flake8_lines:

        # Parse the Flake8 line
        match = re.match(flake8_result_pattern, flake8_line)
        if match is not None:

            # Extract information about the violation
            file = match.group("file")
            line = int(match.group("line")) if match.group("line") is not None else None
            col = match.group("col")
            code = match.group("code")
            message = match.group("message")
            level = MessageLevel.ERROR if strict else MessageLevel.WARNING

            # Check if this Flake8 code is an exception
            if strict:
                if any([code.startswith(element) for element in not_strict_for]):
                    level = MessageLevel.WARNING
            else:
                if any([code.startswith(element) for element in strict_for]):
                    level = MessageLevel.ERROR

            if level == MessageLevel.ERROR:
                should_raise = True

            # Print the formatted message (this format is recognised by
            # Github workflows and will automatically generate code
            # annotations)
            output_lines[level.value].append(
                message_template.format(
                    file=file,
                    line=line,
                    col=col,
                    code=code,
                    message=message,
                    message_title=message_title,
                    level=level.value,
                )
            )

    for message_level, lines in output_lines.items():
        if len(lines) > 0:
            print(f"::group::The following {message_level}s were found")
            print("\n".join(lines))
            print("::endgroup::")

    if should_raise:
        raise Flake8ActionException(f"{len(output_lines['error'])} errors found.")


if __name__ == "__main__":
    main(auto_envvar_prefix="INPUT")
