__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.write("Search")

app = webapp2.WSGIApplication([
    ('/search', Search)
], debug=True)