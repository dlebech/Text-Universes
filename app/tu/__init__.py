# -*- coding: utf-8 -*-
"""
    tu
    ~~~~~~~~~~~~~~~

    Text Universes module.
"""
import webapp2

from main import jinja_env

class BaseHandler(webapp2.RequestHandler):
    def prepare_response(self, template_path, **kwargs):
        temp = jinja_env.get_template(template_path)
        self.response.write(temp.render(kwargs))

    def prepare_json_response(self, js):
        self.response.content_type = 'application/json'
        self.response.write(js)
