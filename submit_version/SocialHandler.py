from Stream import StreamModel
from google.appengine.api import users
import webapp2

SOCIAL_PAGE_TEMPLATE = """\
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
            <td style="background-color:gray"><a href="social">Social</a></td>
        </tr>
    </table>
    <hr size="5" />
    <table>
        <tr>
            <td><img src="http://www.myradiomall.com/mas_assets/ars-Sorry.jpg"></td>
            <td>
                <p style="color:blue"><big>This function has not been supported yet!</big></p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

class Social(webapp2.RequestHandler):
    def get(self):
        self.response.write(SOCIAL_PAGE_TEMPLATE)

app = webapp2.WSGIApplication([
    ('/social', Social)
], debug=True)
