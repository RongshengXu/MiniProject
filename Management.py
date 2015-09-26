__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

MANAGEMENT_PAGE = """\
<html>
  <body>
  <h1>Connex.us</h1>
  <a href='management'>Manage| </a>
  <a href='create'>Create| </a>
  <a href='view'>View |</a>
  <a href='search'>Search |</a>
  <a href='trending'>Trending |</a>
  <a href='social'>Social |</a>
  <a href=%s>Log out </a>
  <br>
  </body>
</html>
"""

ERROR_HTML = """\
<html>
  <body>
  <a href=%s> You need to log in first </a>
  </body>
</html>
"""

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
