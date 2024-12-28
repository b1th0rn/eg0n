#!/bin/bash

rm -rf venv
virtualenv venv #creo il virtual env
./venv/bin/pip install -r ./requirements.txt #richiamando il pip all'interno del veinv, non è necessario attvarlo