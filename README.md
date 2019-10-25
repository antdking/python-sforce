# Python SForce

This is a thin client library for accessing the Salesforce APIs.

## Usage

\# TODO

## Testing

Pytest is used as the testing framework, and tests are structured to loosely define the behaviour of what each component does.

Coverage reports are generated in an effort to identify untested code.
Remember that your tests are **not** complete until all your expected behaviours are covered.

In CI, `tox` is used to ensure we work across Python 3.5-3.7.

In development, you can run `make test`, which is the equivilant of running `python -m pytest`

## Linting

4 linting tools are used in this project:

- `black`, for the unforgiving formatting capabilities.
  If you wish to disobey it, make sure you document why in each case.
- `autoflake`, dead import/code removal
- `isort`, Order is key
- `mypy`, To make sure our components can interact with each other, and to aid IDEs and Mypy users with the development flows. Tests are not currently covered.

The bulk of the linting can be adhered to by running `make autofix`.

You can lint your code by running `make lint`.

## Publishing

We use [flit][flit] for publishing to the PyPI.

By default, we publish to the test PyPI. This is to prevent accidental publishing.

You need to configure your `~/.pypirc` file. An example is:

```ini
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
repository = https://upload.pypi.org/legacy/

[testpypi]
repository = https://test.pypi.org/legacy/
```

To do an actual publish, run `PYPI_INDEX_NAME=pypi make publish`.
This will guide you through the process.


[flit]: https://flit.readthedocs.io/
