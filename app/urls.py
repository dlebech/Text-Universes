# -*- coding: utf-8 -*-
"""URL definitions."""
from webapp2 import Route
from webapp2_extras import routes

routes = [
    routes.RedirectRoute('/', name='index', redirect_to='/main'),
    routes.RedirectRoute('/<universe:\w+>', 
        name='universe-index', 
        handler='tu.site.IndexHandler',
        strict_slash=True),
    routes.PathPrefixRoute('/<universe:\w+>', [
        Route('/text/all', name='texts-all', handler='tu.text.AllTextsHandler'),
        Route('/text/share', name='text-share', handler='tu.text.ShareHandler'),
        Route('/text/twitter',name='text-twitter', handler='tu.text.TwitterHandler')
    ])
]
