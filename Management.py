__author__ = 'rongshengxu'

from PAGE import \
    MANAGEMENT_PAGE, ERROR_HTML

from google.appengine.api import users
import webapp2


class Management(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #self.reponse.write('Hello world!')
        if user:
            #self.reponse.write("Hello world!")
            #self.response.write("Hello World!")
            self.response.write(MANAGEMENT_PAGE % users.create_logout_url('/'))
            #,users.create_logout_url('/'))
        else:
        #    self.response.write("no user")
            self.response.write(ERROR_HTML % users.create_login_url('/'))

app = webapp2.WSGIApplication([
    ('/management', Management)
], debug=True)
