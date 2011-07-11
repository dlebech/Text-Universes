# -*- coding: utf-8 -*-
"""
    tu.db
    ~~~~~~~~~~~~~~~

    Communicates with the Google datastore
"""
import datetime

from google.appengine.ext import db

import tu.config
import tu.security

"""
def login(username, password):
	user = UniverseUser.all().filter('username = ', username)

	if user.count() == 1:
		userinfo = user[0]
		if security.validate_password(password, userinfo.salt, userinfo.password):
			web.ctx.session.login = 1
			web.ctx.session.user = userinfo.username
			web.ctx.session.token = security.tokenize_user(web.ctx.session.user)

def logout():
	web.ctx.session.login = 0
	web.ctx.session.user = ''
	web.ctx.session.token = ''
"""

def get_entries(username, x, y, w, h, universe):
	texts = UniverseText.all()
	if universe:
		texts.filter('universe = ', universe)	
	texts.filter('x >= ', x).filter('x <= ', x+w)
	# GAE only supports inequality on one key. Blah.
	texts = [text for text in texts if text.y >= y and text.y <= y+h]
	texts = [{'txt': text.content, 'date': text.date.__str__(), 'x': text.x, 'y': text.y } for text in texts]
	return texts

def add_entry(username, text, universe):
	coor = find_next_bin(universe)
	text = UniverseText(content = text, date = datetime.datetime.now(), username = username, x = coor[0], y = coor[1], universe = universe)
	text.put()
	return text

def find_next_bin(universe = ''):
	thebin = UniverseBin.all().filter('universe = ', universe).get()

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
	db.delete(UniverseText.all())
	db.delete(UniverseBin.all())
	return 'success'

def add_tag(UniverseText, tag):
	text = UniverseTextTag(tag_text = tag, universe_text = UniverseText)
	text.put()


class UniverseText(db.Model): 
	content = db.TextProperty(required=True)
	date = db.DateTimeProperty(required=True)
	x = db.IntegerProperty(required=True, default=0)
	y = db.IntegerProperty(required=True, default=0)
	username = db.StringProperty()
	universe = db.StringProperty()


class UniverseTextTag(db.Model):
	tag_text = db.TextProperty(required=True)
	universe_text = db.ReferenceProperty(UniverseText, collection_name='tags')


class UniverseUser(db.Model):
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	salt = db.StringProperty(required=True)
	registered = db.DateTimeProperty(required=True, auto_now_add=True)
	name = db.StringProperty()
	email = db.EmailProperty()


class UniverseBin(db.Model):
	x = db.IntegerProperty()
	y = db.IntegerProperty()
	direction = db.IntegerProperty()
	steps = db.IntegerProperty()
	step = db.IntegerProperty()
	universe = db.StringProperty()
