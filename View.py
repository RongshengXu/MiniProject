__author__ = 'rongshengxu'

from Stream import StreamModel
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2

VIEW_PAGE_HTML = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Connex.us</h1>
	<table cellspacing="15">
		<tr>
			<td><a href="management">Manage</a></td>
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

STREAM_ENTRY_TEMPLATE = """\
<td><a href=%s><image src=%s alt=%s height="42" width="42"></image></td>
"""

class View(webapp2.RequestHandler):
    def get(self):
        stream_query = StreamModel.query().order(StreamModel.createTime)
        streams = stream_query.fetch()
        num = 0;
        self.response.write(VIEW_PAGE_HTML)
        self.response.write('<table>')
        for stream in streams:
            if num==0:
                self.response.write("<tr>")
            self.response.write(STREAM_ENTRY_TEMPLATE % (stream.url, stream.coverpageURL, stream.name))
            if num==3:
                self.response.write("</tr>")
                num = 0;
            else:
                num += 1
        self.response.write('</table>')
app = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)