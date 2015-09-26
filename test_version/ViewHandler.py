from Stream import StreamModel
from google.appengine.api import users
import webapp2

VIEW_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html>
<body>
    <h1>Connex.us</h1>
    <table cellspacing="15">
        <tr>
            <td><a href="manage">Manage</a></td>
            <th>|</th>
            <td><a href="create">Create</a></td>
            <th>|</th>
            <td style="background-color:gray"><a href="view">View</a></td>
            <th>|</th>
            <td><a href="search">Search</a></td>
            <th>|</th>
            <td><a href="trending">Trending</a></td>
            <th>|</th>
            <td><a href="social">Social</a></td>
        </tr>
    </table>
    <hr size="5" />
    <h3>View All Streams</h3>
    <table border="1" style="width:100%">
        <tr>
            <td>This line is for the streams</td>
        </tr>
    </table>
</body>
</html>
"""

class View(webapp2.RequestHandler):
    def get(self):
        self.response.write(VIEW_PAGE_TEMPLATE)
        # streams = StreamModel.query(StreamModel.name==users.get_current_uesr()).order(-StreamModel.createTime)

app = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)