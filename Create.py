__author__ = 'rongshengxu'


import cgi
import urllib
from Stream import StreamModel
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import re

CREATE_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Connex.us</h1>
	<table cellspacing="15">
		<tr>
			<td><a href="management">Manage</a></td>
			<th>|</th>
			<td style="background-color:gray"><a href="create">Create</a></td>
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

DEFAULT_CREATE_STREAM_NAME = 'Untitled'

class CreatePage(webapp2.RequestHandler):
    def get(self):
        self.response.write(CREATE_PAGE_TEMPLATE)

class Create(webapp2.RequestHandler):
    def post(self):
        stream_name = self.request.get('streamname', default_value=DEFAULT_CREATE_STREAM_NAME)
        if (len(stream_name)==0):
            stream_name = "Untitled"
        stream_tags = self.request.get('streamtags').split(',')
        stream_subscribers = self.request.get('subscribers').split(',')
        stream_message = self.request.get('context')
        stream_coverpageURL = self.request.get('url')
        stream_query = StreamModel.query(StreamModel.name == stream_name,
                                         StreamModel.author == users.get_current_user()).fetch()
        if (len(stream_query)==0):
            stream = StreamModel()
            stream.name = stream_name
            stream.author = users.get_current_user()
            stream.authorName = users.get_current_user().nickname()
            stream.url = urllib.urlencode({'streamname': stream.name})
            stream.totalPicture = 0;
            if (len(stream_subscribers)>0):
                stream.subscribers = stream_subscribers
            if (len(stream_message)>0):
                stream.message = stream_message
            if(len(stream_tags)>0):
                stream.tag = stream_tags
            if (len(stream_coverpageURL)>0):
                stream.coverpageURL = stream_coverpageURL
            else:
                stream.coverpageURL = "http://static.independent.co.uk/s3fs-public/styles/story_large/public/thumbnails/image/2013/01/24/12/v2-cute-cat-picture.jpg"
            stream.put()
            self.redirect('management')
        else:
            self.redirect('/error')

app = webapp2.WSGIApplication([
    ('/create', CreatePage),
    ('/sign', Create)
], debug=True)
