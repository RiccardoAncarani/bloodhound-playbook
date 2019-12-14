#!/bin/bash

python run-playbook.py
jupyter nbconvert --execute --to html result.ipynb --TemplateExporter.exclude_input=True --ExecutePreprocessor.timeout=-1