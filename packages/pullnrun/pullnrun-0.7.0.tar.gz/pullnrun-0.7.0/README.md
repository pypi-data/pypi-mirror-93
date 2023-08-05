# pullnrun

[![Build Status](https://travis-ci.org/kangasta/pullnrun.svg?branch=master)](https://travis-ci.org/kangasta/pullnrun)
[![Maintainability](https://api.codeclimate.com/v1/badges/7198c6ec9229ca477164/maintainability)](https://codeclimate.com/github/kangasta/pullnrun/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7198c6ec9229ca477164/test_coverage)](https://codeclimate.com/github/kangasta/pullnrun/test_coverage)

A simple python app for running a set of commands from remote sources and pushing result files to remote targets.

## Installing

Ensure that you are using Python >= 3.6 with `python --version`. To install, run:

```bash
pip install pullnrun
```

## Usage

### Examples

See [examples](./examples) for usage examples.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle pullnrun
autopep8 -aaar --in-place pullnrun
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance pullnrun
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source pullnrun/ -m unittest discover -s tst/
coverage report -m
```
