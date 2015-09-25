__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

class Create(webapp2.RequestHandler):
    def get(self):
        self.response.write("Create Stream")

app = webapp2.WSGIApplication([
    ('/create', Create)
], debug=True)
