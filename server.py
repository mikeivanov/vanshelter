#!/usr/bin/env python

import re
import os
import sys
import bottle
import logging
import twitter
import datetime
import threading

from bottle import route

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

UPDATE_INTERVAL = 10.0

logging.basicConfig()
log = logging.getLogger('vanshelter')
log.setLevel(logging.DEBUG)

def now():
    return datetime.datetime.now().isoformat()

#XXX: make it come from an yaml file
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
             last_updated=now(),
             last_id=None,
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
             last_updated=now(),
             last_id=None,
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
             last_updated=now(),
             last_id=None,
             kind="Men and Women",
             notes=None),
        ]

tapi = twitter.Api()

availability_rx = re.compile(r'\[(\d+)/(\d+)\]')
def update_shelter_data(shelter):
    statuces = tapi.GetUserTimeline(screen_name="mike_ivanov",
                                    since_id=shelter['last_id'])
    if len(statuces) > 0:
        last_id = statuces[0].id
        for status in reversed(statuces):
            match = availability_rx.search(status.text)
            if match:
                available, capacity = map(int, match.groups())
                shelter.update(available=available,
                               capacity=capacity,
                               last_updated=now(),
                               last_id=last_id)
                return
        # no match, remember the last id
        shelter.update(last_id=last_id)

@route('/')
def homepage():
    return bottle.static_file("index.html", root=STATIC_ROOT)

@route('/static/:path#.+#')
def server_static(path):
    return bottle.static_file(path, root=STATIC_ROOT)

@route('/api/list')
def api_list():
    return dict(status="ok", data=data)

timer = None
def update_db():
    log.debug("update db")
    for shelter in data:
        update_shelter_data(shelter)
    global timer
    timer = threading.Timer(UPDATE_INTERVAL, update_db)
    timer.start()

app = bottle.app()
app.catchall = False

update_db()
bottle.run(app)
timer.cancel()
