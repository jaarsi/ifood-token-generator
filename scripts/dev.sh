#!/bin/sh -ex
PYTHONPATH=src dotenv run streamlit run --server.runOnSave 1 src/app/main.py