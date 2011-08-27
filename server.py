#!/usr/bin/env python

import re
import os
import sys
import time
import bottle
import logging
import urllib2
import contextlib

from bottle import route

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

logging.basicConfig()
log = logging.getLogger('vanshelter')
log.setLevel(logging.DEBUG)

data = ["empty"]

@route('/')
def homepage():
    return bottle.static_file("index.html", root=STATIC_ROOT)

@route('/static/:filename')
def serve_static(filename):
    return bottle.static_file(filename, root=STATIC_ROOT)

@route('/api/list')
def api_list():
    return dict(ok=true, data=data)


app = bottle.app()
app.catchall = False

bottle.run(app)

