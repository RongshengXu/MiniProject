__author__ = 'rongshengxu'

from Stream import StreamModel
from google.appengine.api import users
import webapp2

CREATE_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Connex.us</h1>
	<table cellspacing="15">
		<tr>
			<th><td><a href="management">View</a></td>Manage</th>
			<td style="background-color:gray"><a href="create">Create</a></td>
			<td><a href="view">View</a></td>
			<td><a href="search">Search</a></td>
			<td><a href="trending">Trending</a></td>
			<td><a href="social">Social</a></td>
		</tr>
	</table>
	<hr size="5" />
	<br>

	<form action="/sign" method="post">
		<table>
			<tr>
				<td><textarea name="streamname" rows="3" cols="60" placeholder = "Lucknow Christian College"></textarea></td>
				<td><textarea name="streamtags" rows="3" cols="60" placeholder = "#LucknowChristianCollege, #1985"></textarea></td>
			</tr>
			<tr>
				<td align="center" valign="top"><b><big>Name Your Stream</big></b></td>
				<td align="center" valign="top"><b><big>Tag Your Stream</big></b></td>
			</tr>
		</table>
		<br>
		<br>
		<br>
		<table>
			<tr>
				<td><textarea name="subscribers" rows="3" cols="60" placeholder = "Input subscribers' emails"></textarea></td>
				<td><textarea name="url" rows="3" cols="60" placeholder = "http://flickr.com/tiger-image.png"></textarea></td>
			</tr>
			<tr>
				<td><textarea name="context" rows="3" cols="60" placeholder="Option message for invite" ></textarea></td>
				<td align="center" valign="top" ><b><big>URL to to Cover Image</big></b></td>
			</tr>
			<tr>
				<td align="center" valign="top"><b><big>Add Subscribers</big></b></td>
			</tr>
		</table>
		<input type="submit" value="Create Stream"></div>
	</form>

</body>
</html>
"""

DEFAULT_CREATE_STREAM_NAME = "Untitled"

class CreatePage(webapp2.RequestHandler):
    def get(self):
        self.response.write(CREATE_PAGE_TEMPLATE)

class Create(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get('streamname', DEFAULT_CREATE_STREAM_NAME)
        stream_tags = self.request.get('streamtags').split(',')
        stream_subscribers = self.request.get('subscribers').split(',')
        stream_message = self.request.get('context')
        stream_coverpageURL = self.request.get('url')
        stream_query = StreamModel.query(StreamModel.name == stream_name, StreamModel.author == users.get_current_user())
        if (len(stream_query)==0):
            stream = stream_query.fectch()
            stream.name = stream_name
            stream.author = users.get_current_user()
            if (len(stream_subscribers)>0):
                stream.subscribers = stream_subscribers
            if (len(stream_message)>0):
                stream.message = stream_message
            if(len(stream_tags)>0):
                stream.tag = stream_tags
            if (len(stream_coverpageURL)>0):
                stream.coverpageURL = stream_coverpageURL
            stream.put()
        else:
            self.redirect('/error')

app = webapp2.WSGIApplication([
    ('/create', CreatePage),
    ('/sign', Create)
], debug=True)
