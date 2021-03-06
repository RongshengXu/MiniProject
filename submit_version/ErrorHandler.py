from Stream import StreamModel
from google.appengine.api import users
import webapp2

ERROR_PAGE_TEMPLATE = """\
<html>
<body>
    <h1>Connex.us</h1>
    <table cellspacing="15">
        <tr>
            <td><a href="manage">Manage</a></td>
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
        </tr>
    </table>
    <hr size="5" />
    <table>
        <tr>
            <td><img src="http://nerdsngeeks.net/wp-content/uploads/2014/01/error.png"></td>
            <td>
                <p style="color:red"><big>Error: you tried to create a new stream whose name is the same as an existing stream;
                operation did not complete.</big></p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

class Error(webapp2.RequestHandler):
    def get(self):
        self.response.write(ERROR_PAGE_TEMPLATE)

app = webapp2.WSGIApplication([
    ('/error', Error)
], debug=True)
