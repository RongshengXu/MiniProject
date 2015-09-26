from google.appengine.api import users
import webapp2

MANAGEMENT_PAGE_TEMPLATE ="""\
<!DOCTYPE html>
<html>
<body>
    <h1>Connex.us</h1>
    <table cellspacing="15">
        <tr>
            <td style="background-color:gray"><a href="manage">Manage</a></td>
            <th>|</th>
            <td><a href="create">Create</a></td>
            <th>|</th>
            <td><a href="view">View</a></td>
            <th>|</th>
            <td><a href="search">Search</a></td>
            <th>|</th>
            <td><a href="trending">Trending</a></td>
            <th>|</th>
            <td><a href="social">Social</a></td>
            <th>|</th>
            <td><a href="%s">%s</a><td>
        </tr>
    </table>
    <hr size="5" />
    <h3>Streams I own</h3>
</body>
</html>
"""

class ManagementPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
            self.response.write(MANAGEMENT_PAGE_TEMPLATE % (url, url_linktext))
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/manage', ManagementPage),
], debug=True)
