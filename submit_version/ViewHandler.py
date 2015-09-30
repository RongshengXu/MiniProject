from Stream import StreamModel
from google.appengine.api import users
from google.appengine.ext import ndb
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
</body>
</html>
"""

# STREAM_ENTRY_TEMPLATE = """\
# <td><a href=%s><image src=%s alt=%s height="42" width="42"></image></td>
# """

STREAM_ENTRY_TEMPLATE = """\
<td>
    <a href="%s">
        <div style = "position:relative;">
            <img src="%s" height="150" width="150"></img>
            <div style = "position: relative; left:65px; top:0px">%s</div>
        </div>
    </a>
</td>
"""

class View(webapp2.RequestHandler):
    more = True
    def get(self):
        self.response.write(VIEW_PAGE_TEMPLATE)
        stream_query = StreamModel.query().order(StreamModel.createTime)
        streams = stream_query.fetch()
        num = 0
        self.response.write('<table border="0" style="width:100%">')
        if len(streams) > 0:
            self.more = True
            for stream in streams:
                if num==0:
                    self.response.write("<tr>")

                self.response.write(STREAM_ENTRY_TEMPLATE % (stream.url, stream.coverpageURL, stream.name))

                if num==3:
                    self.response.write("</tr>")
                    num = 0
                else:
                    num += 1

        else:
            self.response.write("<tr><td>No streams are available</td></tr>")
        self.response.write('</table>')

app = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)