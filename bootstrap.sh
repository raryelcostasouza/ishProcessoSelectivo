#!/bin/bash
export SPOTIPY_CLIENT_ID='6198d3c4a2cc4ca08334d6f1c097637d'
export SPOTIPY_CLIENT_SECRET='dc224e5a99664b6cbb4dd18b58179db7'

export FLASK_APP=./safelabs/index.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0
