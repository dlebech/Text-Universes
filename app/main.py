# -*- coding: utf-8 -*-
"""WSGI app setup."""
import os

from webapp2 import WSGIApplication
import jinja2

from config import config
from urls import routes

# Is this the development server?
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

app = WSGIApplication(routes, config=config, debug=debug)
