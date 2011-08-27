#!/bin/sh

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
source env/bin/activate
exec python server.py
