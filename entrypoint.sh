#!/bin/bash -l

# Put the config in a file
if [ -n "$INPUT_FLAKE8_CONFIG" ]
then
    echo -e "$INPUT_FLAKE8_CONFIG" > .flake8
fi
echo "::group::Flake8 config"
cat .flake8
echo "::endgroup::"

# Install additional package (if applicable)
if [ -n "$INPUT_ADDITIONAL_PACKAGES" ]
then
    echo "::group::Additional packages"
    pip install -U $INPUT_ADDITIONAL_PACKAGES
    echo "::endgroup::"
fi

# Generate Flake8 output if there isn't any
if [ -z "$FLAKE8_OUTPUT" ]
then
    echo "::group::Flake8"
    flake8 --exit-zero --verbose > flake8_results.txt
    echo "::endgroup::"
fi

# Run the command to parse the Flake8 output
python main.py
