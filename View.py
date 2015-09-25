__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

class View(webapp2.RequestHandler):
    def get(self):
        self.response.write("View")

app = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)