__author__ = 'rongshengxu'

from Stream import StreamModel
from google.appengine.api import users
import webapp2

VIEW_PAGE_HTML = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Connex.us</h1>
	<table cellspacing="15">
		<tr>
			<th>Manage</th>
			<td><a href="createstream">Create</a></td>
			<td style="background-color:gray"><a href="viewallstream">View</a></td>
			<td><a href="search">Search</a></td>
			<td><a href="trending">Trending</a></td>
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
        streams = StreamModel.query(StreamModel.name==users.get_current_uesr()).order(-StreamModel.createTime)

app = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)