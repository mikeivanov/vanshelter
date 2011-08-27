#!/bin/sh
set -o nounset
set -o errexit
virtualenv env
pip -E env install -r requirements.txt
echo "Now activate the environment: source env/bin/activate"
