# Flake8-Action
This Github Action makes it possible to run Flake8 (optionally with plugins) and use the output to annotate code in pull requests.

## Usage
You can use `uses: gijswobben/flake8-action@main` in a Github Actions workflow to check your Python code with Flake8. Additional options can be configured in the `with:` section (see examples for details).

| Parameter | Description |
| ---:|:--- |
| `strict` | If strict is True the pipeline will fail when a Flake8 violation is encountered. Boolean, defaults to: `false`. |
| `strict_for` | Specify individual codes to apply strict rules for. Formatted as comma separated string. |
| `not_strict_for` | Specify individual codes to NOT apply strict rules for. Formatted as comma separated string. |
| `message_title` | Custom title for the warnings/errors in the code annotations. Defaults to: `"Flake8 issue found"` |
| `flake8_output` | If specified, don't run the Flake8 command but use the value of this input as the Flake8 content to parse. |
| `additional_packages` | If specified, install these packages (e.g. Flake8 plugins) before running the Flake8 command. |
| `flake8_config` | Flake8 configuration in `.flake8` format. |

## Full example
This a full example to showcase the different parameters that can be used with this Github Action.

```yaml
name: Code quality
"on": ["push"]

jobs:
  flake8:
    name: Flake8 tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - uses: gijswobben/flake8-action@main
        with:
          strict: true
          strict_for: "E501"
          not_strict_for: "E502,E503"
          message_title: "Flake8 error found"
          flake8_config: |
            [flake8]
            exclude = examples/ tests/
            max-line-length = 88
            extend-ignore =
                # See https://github.com/PyCQA/pycodestyle/issues/373
                E203,
          additional_packages: pep8-naming==0.13.2 flake8-annotations==2.9.1 darglint==1.8.1 flake8-bugbear==22.10.27
```

More examples can be found in the `.github/workflows` folder of this repository.

Some changes