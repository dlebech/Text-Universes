# -*- coding: utf-8 -*-
"""
    tu.security
    ~~~~~~~~~~~~~~~

    Security functions
"""
import time 
from hashlib import sha256
from math import ceil
from random import choice

import tu.config

def create_nonce():
	i = nonce_tick()
	return sha256(config.NONCE_SALT + `i`).hexdigest()

def nonce_tick():
	return ceil(time.time() / 86400)

def tokenize_user(user):
	nonce = create_nonce()
	return sha256(sha256(nonce + config.LOGGED_IN_SALT).hexdigest() + user).hexdigest()

def validate_session():
	user = web.ctx.session.user
	token = web.ctx.session.token
	if tokenize_user(user) == token:
		return True
	else:
		return False

def loggedin():
	if web.ctx.session.login == 1 and validate_session():
		return True
	else:
		return False

def validate_password(trypassword, salt, realpassword):
	passw = encode_password(trypassword, salt)
	if (passw == realpassword):
		return True;
	else:
		return False;

def encode_password(password, salt):
	"""Encodes the given password for authentication"""
	return sha256(sha256(salt + config.AUTH_SALT).hexdigest() + password).hexdigest()


def generate_salt(max = 15):
	"""Generates a password salt."""
	clist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
	salt = ''.join([choice(clist) for i in range(0, max)])
	return salt
