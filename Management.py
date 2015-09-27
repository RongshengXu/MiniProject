__author__ = 'rongshengxu'

from Stream import StreamModel, PictureModel
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import ndb
import webapp2

MANAGEMENT_PAGE = """\
<!DOCTYPE html>
<html>
<body>
	<h1>Connex.us</h1>
	<table cellspacing="15">
		<tr>
			<td style="background-color:gray"><a href="management">Manage</a></td>
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
  	<h3>Streams I own</h3>
</body>
</html>
"""

ERROR_HTML = """\
<html>
  <body>
  <a href=%s> You need to log in first </a>
  </body>
</html>
"""

STREAM_I_OWN_ENTRY = """\
<br><a href=%s>%s</a>  %s  %s</br>
"""

class Management(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #self.reponse.write('Hello world!')
        if user:
            self.response.write(MANAGEMENT_PAGE)
            stream_query = StreamModel.query(StreamModel.author==user).order(-StreamModel.createTime).fetch()
            for stream in stream_query:
                self.response.write(STREAM_I_OWN_ENTRY % (stream.url, stream.name,
                                                          stream.lastUpdated, str(stream.totalPicture)))
                self.response.write('<form action="/deletestream", method="post">' +
                                    '<td><input type="checkbox" name="deleteStream", value="%s"></>'% stream.name)
            self.response.write('<input type="submit" value ="Delete Checked"></form>')
            self.response.write("<a href=%s> log out </a> " % users.create_logout_url('/'))
        else:
            self.response.write(ERROR_HTML % users.create_login_url('/'))

class deleteStream(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        streams = self.request.get_all("deleteStream")
        if len(streams)>0:
            stream_query = StreamModel.query(StreamModel.name.IN(streams), StreamModel.author==users.get_current_user())
            streams = stream_query.fetch()
            for stream in streams:
                pictures = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1",
                                  db.Key.from_path('StreamModle', stream.name))
                db.delete(pictures)
            ndb.delete_multi(ndb.put_multi(streams))
        self.redirect(returnURL)

app = webapp2.WSGIApplication([
    ('/management', Management),
    ('/deletestream', deleteStream)
], debug=True)
