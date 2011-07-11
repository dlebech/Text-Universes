import web, cluster, db

urls = (
	'/removeall', 'remove_all')

#class cluster_creation:
#	"""Creates clusters of all text submitted"""
#	def GET(self):
#		return cluster.start()

class remove_all:
	"""Removes all pieces of text from the db. Only used for debugging"""
	def GET(self):
		return db.remove_all()

cronapp = web.application(urls, locals())
