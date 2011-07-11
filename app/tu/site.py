# -*- coding: utf-8 -*-
"""
    tu.site
    ~~~~~~~~~~~~~~~

    Basic site handling
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin

class IndexHandler(RequestHandler, Jinja2Mixin):
    def get(self, universe = 'Text Universes'):
        return self.render_response('index.html', universe = universe)

class LoginHandler(RequestHandler, Jinja2Mixin):
    def get(self, universe = ''):
        return self.render_response('login.html')

    def post(self, universe = ''):
        username, password = self.request.form.get('usernam'), self.request.form.get('password')
        db.login(p.username, p.password)
        return render_login()

"""
class logout:
    def GET(self):
        db.logout()
        return render_login()

def render_login():
    if (security.loggedin()):
        return render.loggedin(get_user_dict()['username'])
    else:
        return render.login()

def get_user_dict():
    userinfo = web.ctx.session.user.split(';')
    if (len(userinfo) == 1):
        return { 'username': userinfo[0] }
    else:
        return { 'username': '' }
"""
