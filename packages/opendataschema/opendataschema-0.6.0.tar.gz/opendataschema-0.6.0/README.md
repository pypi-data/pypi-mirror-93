# Open Data Schema Python client

[![PyPI](https://img.shields.io/pypi/v/opendataschema.svg)](https://pypi.python.org/pypi/opendataschema)

## Install

```bash
pip install opendataschema
```

## Usage

Note: the `schema.json` file can be given as a file path or an URL.

```bash
opendataschema schema.json list
opendataschema schema.json show
opendataschema schema.json show --name <schema_name>
opendataschema schema.json show --versions
```

## Configuration

Environment variables:

- `CATALOG_SCHEMA`: customise the URL or file path of the JSON schema to use to validate the catalog JSON file

## GitHub API Rate limiting

Because of to the [rate limiting strategy](https://developer.github.com/v3/#rate-limiting) of GitHub API, you may encounter a `github.GithubException.RateLimitExceededException`. To avoid that, generate a private access token in your [tokens settings page](https://github.com/settings/tokens), and set the `GITHUB_ACCESS_TOKEN` environment variable.
