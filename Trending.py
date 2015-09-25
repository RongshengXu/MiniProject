__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

class Trending(webapp2.RequestHandler):
    def get(self):
        self.response.write("Trending")

app = webapp2.WSGIApplication([
    ('/trending', Trending)
], debug=True)