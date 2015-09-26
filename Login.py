__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

LOGIN_PAGE_HTML = """\
<html>
  <body>
    <h1>Welcome to Connexus!</h1>
    <h2>Share the world!</h2>
    <a href=%s> Log in </a>
   </body>
</html>
"""

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