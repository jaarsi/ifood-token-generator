#!/bin/sh -ex
isort --profile black src
black src
ruff check src