__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

class Social(webapp2.RequestHandler):
    def get(self):
        self.response.write("Social")

app = webapp2.WSGIApplication([
    ('/social', Social)
], debug=True)