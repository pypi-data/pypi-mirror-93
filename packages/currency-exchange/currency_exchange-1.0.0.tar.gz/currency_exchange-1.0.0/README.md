# Project name or package name or short description 

Long description about project or package


## Supported Python Interpreters
Best practice adding information about supported Python interpreters versions
You could omit information about CPython: CPython 3.5 == Python 3.5.
If you test and plan to support other interpreters mention it. Like PyPy3 - Supported

Basic table

| Major Version | Supported | Test Passed |
|---------------|-----------|-------------|
| Python 3.6    |    Yes    |     Yes     |
| Python 3.7    |    Yes    |     Yes     |
| Python 3.8    |    Yes    |     Yes     |
| Python 3.9    |    Yes    |     Yes     |

It could replace by badges (for information how to generate see [pybadges](https://github.com/google/pybadges) )

![versions](https://i.ibb.co/WGxGSW5/badge.png)

## Install

On this section you could add additional information about private or public PyPI repository

```shell script
pip install my-awesome-package \
  --trusted-host example.org \
  --extra-index-url https://example.org/pypi/simple
```    


## How to use
Some samples or link to documentation

```python

```

## Setup developer environments
For local developing you must install all packages from requirements-dev.txt

```shell
make dev
```

## Setup developers environments
For local developing you must install all packages from requirements-dev.txt
```shell
make dev
```

### Tests

Run tests quickly with the default Python
```shell
make test
```

Check style with flake8
```shell
make lint
```

Check style, coverage and tests
```shell
make test-all
```

Run tests on every Python version with tox
```shell
make tox
```


### Build packages
Without test
```shell
make dist
```

Build after coverage, check style and test
```shell
make dist-with-test
```
