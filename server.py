#!/usr/bin/env python

import re
import os
import csv
import bottle
import logging
import twitter
import datetime
import threading

from bottle import route

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

UPDATE_INTERVAL = 30.0

logging.basicConfig()
log = logging.getLogger('vanshelter')
log.setLevel(logging.DEBUG)

tapi = twitter.Api()

def now():
    return datetime.datetime.now().isoformat()

def load_data():
    data = []
    reader = csv.reader(open('shelters.csv', 'rb'))
    for id, (twitter, name, org, addr, 
             phone, capacity, kind) in enumerate(reader):
        if id > 0:
            data.append(dict(id=id,
                             twitter=(None if twitter.strip() == "" 
                                           else twitter),
                             name=name,
                             organization=org,
                             address=None if addr == 'n/a' else addr,
                             phone=phone,
                             open_from=0,
                             open_until=0,
                             capacity=int(capacity),
                             available=0,
                             last_updated=now(),
                             last_id=None,
                             kind=kind))
    return data

availability_rx = re.compile(r'\[(\d+)/(\d+)\]')
def update_shelter_data(shelter):
    #XXX: add error handling
    statuces = tapi.GetUserTimeline(screen_name=shelter['twitter'],
                                    since_id=shelter['last_id'],
                                    count=10)
    if len(statuces) > 0:
        last_id = statuces[0].id
        for status in statuces:
            match = availability_rx.search(status.text)
            if match:
                available, capacity = map(int, match.groups())
                shelter.update(available=available,
                               capacity=capacity,
                               last_updated=now(),
                               last_id=last_id)
                log.debug("updated %s" % shelter['id'])
                return
        # no match, remember the last id
        shelter.update(last_id=last_id)

timer = None
def update_db():
    log.debug("update db")
    for shelter in data:
        if shelter['twitter']:
            update_shelter_data(shelter)
    global timer
    timer = threading.Timer(UPDATE_INTERVAL, update_db)
    timer.start()

# our "database"
data = load_data()

@route('/')
def homepage():
    return bottle.static_file("index.html", root=STATIC_ROOT)

@route('/static/:path#.+#')
def server_static(path):
    return bottle.static_file(path, root=STATIC_ROOT)

@route('/api/list')
def api_list():
    return dict(status="ok", data=data)

app = bottle.app()
app.catchall = False

update_db()
bottle.run(app)
timer.cancel()

