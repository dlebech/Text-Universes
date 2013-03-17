# -*- coding: utf-8 -*-
"""
    tu.site
    ~~~~~~~~~~~~~~~

    Basic site handling
"""
from tu import BaseHandler

class IndexHandler(BaseHandler):
    def get(self, universe = 'Text Universes'):
        return self.prepare_response('index.html', universe = universe)
