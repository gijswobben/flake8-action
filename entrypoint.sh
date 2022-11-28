#!/bin/bash -l

# Put the config in a file
if [ -n "$INPUT_FLAKE8_CONFIG" ]
then
    echo -e "$INPUT_FLAKE8_CONFIG" > .flake8
fi

echo "::group::Using Flake8 config"
cat .flake8
echo "::endgroup::"

# Install additional package (if applicable)
if [ -n "$ADDITIONAL_PACKAGES" ]
then
    echo "Install additional packages"
    pip install -U $ADDITIONAL_PACKAGES
fi

# Generate Flake8 output if there isn't any
if [ -z "$FLAKE8_OUTPUT" ]
then
    echo "Running Flake8"
    flake8 --exit-zero > flake8_results.txt
fi

# Run the command to parse the Flake8 output
python main.py
