# -*- coding: utf-8 -*-
"""
    tu.text
    ~~~~~~~~~~~~~~~

    Handles all text IO.
"""
import re
import urllib
from cgi import escape
import json

from google.appengine.api import urlfetch

import tu.db 
import tu.config
from tu import BaseHandler

class AllTextsHandler(BaseHandler):
    def get(self, universe = ''):
        x = self.request.GET.get('x') or '0'
        y = self.request.GET.get('y') or '0'
        w = self.request.GET.get('w') or '400'
        h = self.request.GET.get('h') or '400'
        thetexts = tu.db.get_entries('', int(x), int(y), int(w), int(h), universe)
        self.prepare_json_response(json.dumps(thetexts))


class ShareHandler(BaseHandler):
    def post(self, universe = ''):
        text, answer = escape(self.request.POST.get('text')), self.request.POST.get('answer')
        if text:
            if re.search(tu.config.DIRTY_WORDS_RE, text.lower()):
                return self.prepare_response('text_shared_error.html', message = 'Please do not use dirty words.')
            elif answer == 'fourth':
                #if (security.loggedin()):
                #    db.add_entry(get_user_dict()['username'], text, universe)
                #else:
                tu.db.add_entry('', text, universe)
                return self.prepare_response('text_shared.html')
            else:
                return self.prepare_response('text_shared_error.html', message = 'Your answer is not correct.')
        else:
            return self.prepare_response('text_shared_error.html', message = 'You cannot save empty text.')

    def get(self, universe = ''):
        return self.prepare_response('share_text.html')


class TwitterHandler(BaseHandler):
    def post(self, universe = ''):
        text, answer = self.request.POST.get('text'), self.request.POST.get('answer')
        if text:
            if re.search(tu.config.DIRTY_WORDS_RE, text.lower()):
                return self.prepare_response('text_shared_error.html', message = 'Please do not use dirty words.')
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
                            text.tags.append(tag[1:])
                        text.put()
                
                    return self.prepare_response('text_shared.html')
                else:
                    return self.prepare_response('text_shared_error.html', message = 'Could not fetch from Twitter.')
            else:
                return self.prepare_response('text_shared_error.html', message = 'Your answer is not correct.')
        else:
            return self.prepare_response('text_shared_error.html', message = 'You cannot save an empty keyword.')
