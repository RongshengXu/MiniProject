__author__ = 'rongshengxu'

from google.appengine.api import users
import webapp2

TRENDING_PAGE_TEMPLATE = """\
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
			<td><a href="view">View</a></td>
			<th>|</th>
			<td><a href="search">Search</a></td>
			<th>|</th>
			<td  style="background-color:gray"><a href="trending">Trending</a></td>
			<th>|</th>
			<td><a href="social">Social</a></td>
		</tr>
	</table>
	<hr size="5" />
  	<h3>Top 3 Trending Streams</h3>
	<table border="1" style="width:100%">
		<tr>
			<td>This line is for the top 3 trending streams</td>
		</tr>
	</table>
	<hr>
	<h3>Email reending report</h3>
  	<form action="/update" method="post">
		<input type="radio" name="frequency" value="No reports" checked>No reports</input><br>
		<input type="radio" name="frequency" value="Every 5 minutes">Every 5 minutes</input><br>
		<input type="radio" name="frequency" value="Every 1 hour">Every 1 hour</input><br>
		<input type="radio" name="frequency" value="Every day">Every day</input><br>
		<input type="submit" value="Update rate">
    </form>
</body>
</html>
"""

class Trending(webapp2.RequestHandler):
    def get(self):
        self.response.write(TRENDING_PAGE_TEMPLATE)

app = webapp2.WSGIApplication([
    ('/trending', Trending)
], debug=True)