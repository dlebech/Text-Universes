# -*- coding: utf-8 -*-
"""
    tu.text
    ~~~~~~~~~~~~~~~

    Handles all text IO.
"""
import re
import urllib
from cgi import escape

from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin
from tipfy.utils import render_json_response

from google.appengine.api import urlfetch
from django.utils import simplejson as json
import tu.db 
import tu.config

class AllTextsHandler(RequestHandler):
    def post(self, universe = ''):
        x = self.request.form.get('x') or '0'
        y = self.request.form.get('y') or '0'
        w = self.request.form.get('w') or '400'
        h = self.request.form.get('h') or '400'
        thetexts = tu.db.get_entries('', int(x), int(y), int(w), int(h), universe)
        return render_json_response(json.dumps(thetexts))

"""
class MyTextsHandler:
    def post(self):
        if (security.loggedin()):
            thetexts = db.get_entries(get_user_dict()['username'])
            return render.user_texts(thetexts)
        else:
            return ''
"""

class ShareHandler(RequestHandler, Jinja2Mixin):
    def post(self, universe = ''):
        text, answer = escape(self.request.form.get('text')), self.request.form.get('answer')
        if text:
            if re.search(tu.config.DIRTY_WORDS_RE, text.lower()):
                return self.render_response('text_shared_error.html', message = 'Please do not use dirty words.')
            elif answer == 'fourth':
                #if (security.loggedin()):
                #    db.add_entry(get_user_dict()['username'], text, universe)
                #else:
                tu.db.add_entry('', text, universe)
                return self.render_response('text_shared.html')
            else:
                return self.render_response('text_shared_error.html', message = 'Your answer is not correct.')
        else:
            return self.render_response('text_shared_error.html', message = 'You cannot save empty text.')

    def get(self, universe = ''):
        return self.render_response('share_text.html')

class TwitterHandler(RequestHandler, Jinja2Mixin):
    def post(self, universe = ''):
        text, answer = self.request.form.get('text'), self.request.form.get('answer')
        if text:
            if re.search(tu.config.DIRTY_WORDS_RE, text.lower()):
                return self.render_response('text_shared_error.html', message = 'Please do not use dirty words.')
            elif answer == 'fourth':
                parameters = {
                    "q" : text
                }
                url = tu.config.TWITTER_URL + urllib.urlencode(parameters)
                result = urlfetch.fetch(url)
                if result.status_code == 200:
                    data = json.loads(result.content)
                    for i in data["results"]:
                        text = tu.db.add_entry('', "<b>" + i["from_user"] + "</b><br/>" + i["text"], universe)
                        for tag in re.findall('#\S+', i["text"]):
                            tu.db.add_tag(text, tag[1:])
                
                    return self.render_response('text_shared.html')
                else:
                    return self.render_response('text_shared_error.html', 'Could not fetch from Twitter.')
            else:
                return self.render_response('text_shared_error.html', message = 'Your answer is not correct.')
        else:
            return self.render_response('text_shared_error.html', 'You cannot save an empty keyword.')
