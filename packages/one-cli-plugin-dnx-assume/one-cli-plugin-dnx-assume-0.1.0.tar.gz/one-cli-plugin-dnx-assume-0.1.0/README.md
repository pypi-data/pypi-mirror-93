# plugin-dnx-assume

This is a one-cli plugin that adds extra assume role entry command to the CLI.

![Build](https://github.com/DNXLabs/plugin-dnx-assume/workflows/Build/badge.svg)
[![PyPI](https://badge.fury.io/py/one-cli-plugin-dnx-assume.svg)](https://pypi.python.org/pypi/one-cli-plugin-dnx-assume/)
[![LICENSE](https://img.shields.io/github/license/DNXLabs/plugin-dnx-assume)](https://github.com/DNXLabs/plugin-dnx-assume/blob/master/LICENSE)


## Configuration

```yaml
# one.yaml
plugins:
  dnx-assume:
    package: one-cli-plugin-dnx-assume
    version: 0.1.0
    module: 'plugin_dnx_assume'
    parameters:
      aws_role: <redact>
      aws_account_id: <redact>
```

## Usage

```bash
one dnx-assume
```

## Development

#### Dependencies

- Python 3

#### Python Virtual Environment

```bash
# Create environment
python3 -m venv env

# To activate the environment
source env/bin/activate

# When you finish you can exit typing
deactivate
```

#### Install dependencies

```bash
pip3 install --editable .
```

## Author

Managed by [DNX Solutions](https://github.com/DNXLabs).

## License

Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/plugin-dnx-assume/blob/master/LICENSE) for full details.