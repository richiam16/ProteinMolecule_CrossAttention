#!/bin/bash
set -e

conda env create --file=environment.yml
mamba activate
python -m ipykernel install --user --name molzy

