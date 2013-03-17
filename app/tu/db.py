# -*- coding: utf-8 -*-
"""
    tu.db
    ~~~~~~~~~~~~~~~

    Communicates with the Google datastore
"""
from google.appengine.ext import ndb

import tu.config
import tu.security

def get_entries(username, x, y, w, h, universe):
    texts = UniverseText.query()
    if universe:
        texts = texts.filter(UniverseText.universe == universe)	
    texts = texts.filter(UniverseText.x >= x).filter(UniverseText.x <= x+w)
    # GAE only supports inequality on one key. Blah.
    texts = texts.fetch()
    texts = [{'txt': text.content, 
              'date': str(text.date), 
              'x': text.x, 
              'y': text.y, 
              'tags': text.tags }
              for text in texts
              if text.y >= y and text.y <= y+h]
    return texts

def add_entry(username, text, universe):
    coor = find_next_bin(universe)
    text = UniverseText(content = text, x = coor[0], y = coor[1], universe = universe)
    text.put()
    return text

def find_next_bin(universe = ''):
    thebin = UniverseBin.query().filter(UniverseBin.universe == universe).get()

    # Base case, create the new UniverseBin
    if not thebin:
        thebin = UniverseBin(x = 0, y = 0, direction = 1, steps = 1, step = 0, universe = universe)
        thebin.put()
        return [thebin.x, thebin.y]

    # Calculate new bin position
    if thebin.direction == 1:
        thebin.x += tu.config.BIN_SIZE[0] 
    elif thebin.direction == 2:
        thebin.y += tu.config.BIN_SIZE[1]
    elif thebin.direction == 3:
        thebin.x -= tu.config.BIN_SIZE[0]
    else:
        thebin.y -= tu.config.BIN_SIZE[1]

    thebin.step += 1

    # If we have stepped enough
    if thebin.step == thebin.steps:
        # Possibly change steps
        if thebin.direction in [2, 4]:
            thebin.steps += 1

        # Change direction and reset number of steps
        thebin.direction = (thebin.direction % 4) + 1
        thebin.step = 0

    # Updates the db
    thebin.put()

    return [thebin.x, thebin.y]

def remove_all():
    ndb.delete(UniverseText.all())
    ndb.delete(UniverseBin.all())
    return 'success'


class UniverseText(ndb.Model): 
    date = ndb.DateTimeProperty(auto_now_add=True)
    universe = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    x = ndb.IntegerProperty(default=0)
    y = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)


class UniverseBin(ndb.Model):
    x = ndb.IntegerProperty()
    y = ndb.IntegerProperty()
    direction = ndb.IntegerProperty()
    steps = ndb.IntegerProperty()
    step = ndb.IntegerProperty()
    universe = ndb.StringProperty()
