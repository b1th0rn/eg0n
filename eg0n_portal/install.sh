#!/bin/bash

rm -rf venv
virtualenv venv #create the virtual environment
./venv/bin/pip install -r ./requirements.txt #recall the venv folder to install the requirements