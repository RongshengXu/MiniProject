from Stream import StreamModel
from google.appengine.api import users
import webapp2

SEARCH_PAGE_TEMPLATE = """\
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
            <td><a href="view">View</a></td>
            <th>|</th>
            <td style="background-color:gray"><a href="search">Search</a></td>
            <th>|</th>
            <td><a href="trending">Trending</a></td>
            <th>|</th>
            <td><a href="social">Social</a></td>
        </tr>
    </table>
    <hr size="5" />
    <h3>Search Streams</h3>
    <form action="/showsearch" method="get">
        <input type="search" name="searchStream" placeholder="Lucknow"><br>
        <input type="submit" value="Search">
    </form>
</body>
</html>
"""

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.write(SEARCH_PAGE_TEMPLATE)

app = webapp2.WSGIApplication([
    ('/search', Search)
], debug=True)