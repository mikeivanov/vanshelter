#!/bin/bash
set -o errexit
virtualenv env
source env/bin/activate
pip -E env install -r requirements.txt
echo "Now activate the environment: source env/bin/activate"
