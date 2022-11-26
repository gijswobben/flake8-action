# import os


# def main():
#     my_input = os.environ["INPUT_MYINPUT"]
#     my_output = f"Hello {my_input}"
#     print(f"::set-output name=myOutput::{my_output}")


# if __name__ == "__main__":
#     main()

from __future__ import annotations

import re
from pathlib import Path

flake8_result_pattern = re.compile(
    r"(?P<file>.+):(?P<line>\d+):(?P<col>\d+): (?P<code>[A-Z]+\d+)\s(?P<message>.+)"
)


def main():

    # Read the Flake8 results
    flake8_output_path = Path("flake8_results.txt")
    flake8_lines = flake8_output_path.read_text().splitlines()

    # Go over every result in the Flake8 results and print a warning if
    # the file/line combination changed in this branch
    title = "Flake8 issue found"
    for flake8_line in flake8_lines:

        # Parse the Flake8 line
        match = re.match(flake8_result_pattern, flake8_line)
        if match is not None:
            file = match.group("file")
            line = int(match.group("line")) if match.group("line") is not None else None
            col = match.group("col")
            code = match.group("code")
            message = match.group("message")

            # If the file/line combination was changed according to git
            # diff, and Flake8 raised something
            print(
                f"::warning file={file},line={line},col={col},title={title}::{code} - {message}"
            )


if __name__ == "__main__":
    main()