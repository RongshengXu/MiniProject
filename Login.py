__author__ = 'rongshengxu'

from PAGE import LOGIN_PAGE_HTML
from google.appengine.api import users
import webapp2

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            #self.redirect('management')
            self.response.out.write(LOGIN_PAGE_HTML % users.create_logout_url('/'))
        else:
            self.response.write((LOGIN_PAGE_HTML) %
                                users.create_login_url('/management'))

app = webapp2.WSGIApplication([
    ('/', LoginPage),
], debug=True)
# remove debug=True before deploying the final version