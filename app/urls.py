# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule, HandlerPrefix, BaseConverter

rules = [
    Rule('/', name='index', redirect_to= '/main'),
    Rule('/<string:universe>/', name='index', handler='tu.site.IndexHandler'),
    Rule('/<string:universe>/login', 'site-login', handler='tu.site.LoginHandler'),
    Rule('/pretty', name='hello-world-pretty', handler='hello_world.handlers.PrettyHelloWorldHandler'),
    HandlerPrefix('tu.text.', [
        Rule('/<string:universe>/text/all', 'texts-all', handler='AllTextsHandler'),
        Rule('/<string:universe>/text/mine', 'texts-mine', handler='MyTextsHandler'),
        Rule('/<string:universe>/text/share', 'text-share', handler='ShareHandler'),
        Rule('/<string:universe>/text/twitter','text-twitter', handler='TwitterHandler'),
    ]),
]
