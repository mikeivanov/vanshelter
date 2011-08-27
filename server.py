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

# our "database"
data = [dict(id="bcdata_bridge",
             name="Bridge Women's Emergency Shelter",
             organization="Atira Women's Resource Society",
             address=None,
             phone="604-331-1407",
             open_from=0,
             open_until=0,
             capacity=12,
             available=0,
             kind="Women",
             notes=None),

        dict(id="bcdata_st_elizabeth",
             name="St. Elizabeth Home",
             organization="St. James Community Services Society",
             address=None,
             phone="604-606-0412",
             open_from=0,
             open_until=0,
             capacity=32,
             available=0,
             kind="Women and their Children",
             notes=None),

        dict(id="bcdata_lookout",
             name="Lookout Downtown Shelter",
             organization="Lookout Emergency Aid Society",
             address="346 Alexander Street",
             phone="604-681-9126",
             open_from=0,
             open_until=0,
             capacity=46,
             available=0,
             kind="Men and Women",
             notes=None),
        ]

@route('/')
def homepage():
    return bottle.static_file("index.html", root=STATIC_ROOT)

@route('/static/:filename')
def serve_static(filename):
    return bottle.static_file(filename, root=STATIC_ROOT)

@route('/api/list')
def api_list():
    return dict(status="ok", data=data)

app = bottle.app()
app.catchall = False

bottle.run(app)

