__author__ = 'rongshengxu'

from Stream import PictureModel, StreamModel
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.ext import blobstore

import webapp2
import re
import urllib

VIEW_SINGLE_PAGE_HTML = """\
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
  	<h3>View A Single stream</h3>
	<table border="1" style="width:100%">
		<tr>
			<td>This line is for the pictures in this stream</td>
		</tr>
	</table>
</body>
</html>
"""

UPLOAD_ENTRY_TEMPLATE = """\
<form action="/upload" method="post" enctype="multipart/form-data">
		Upload File:
		<input type="file"  name="file" >
		<br>
		<input type="submit" name="submit" value="Submit">
</form>
"""

MORE_ENTRY_TEMPLATE = """\
	<form action="%s" ,method="post">
		<input type="submit" value="More Pictures">
	</form>
"""

PICTURE_ENTRY_TEMPLATE = """\
<td><img src="pic?pic_id=%s"></img></td>
"""

class ViewSingle(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.write("Hello")
        stream_name = re.findall('%3D(.*)', self.request.url)[0]
        #self.response.write(stream_name)
        self.response.write(VIEW_SINGLE_PAGE_HTML)
        self.response.write('<h3>%s</h3>' % stream_name)
        stream_query = StreamModel.query(StreamModel.name==stream_name, StreamModel.author==user)
        stream = stream_query.fetch()[0]
        picture_query = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1 ORDER BY uploadDate DESC LIMIT 5",
                                  db.Key.from_path('StreamModel', stream_name))
        for picture in picture_query:
            self.response.write(PICTURE_ENTRY_TEMPLATE % picture.key())
        morePictureURL = urllib.urlencode({'showmore':user.nickname()+"=="+stream_name})
        self.response.write(MORE_ENTRY_TEMPLATE % morePictureURL)
        self.response.write(UPLOAD_ENTRY_TEMPLATE)

class ViewPictureHandler(webapp2.RequestHandler):
    def get(self):
        pic = db.get(self.request.get('pic_id'))
        self.response.out.write(pic.picture)

class Upload(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        picture = self.request.get('file')
        if (len(picture)>0):
            stream_name = re.findall('=(.*)', returnURL)[0]
            stream_query = StreamModel.query(StreamModel.name==stream_name, StreamModel.author==users.get_current_user())
            stream = stream_query.fetch()[0]
            stream.totalPicture = stream.totalPicture + 1
            user_picture = PictureModel(parent = db.Key.from_path('StreamModel', stream_name))
            user_picture.id = str(stream.totalPicture)
            picture = images.resize(picture, 320, 400)
            user_picture.picture = db.Blob(picture)
            user_picture.put()
            stream.put()
            #user_picture.picture = db.Blob(image)
        self.redirect(returnURL)

class ShowMore(webapp2.RequestHandler):
    def get(self):
        user = re.findall('%3D(.*)%3D%3D', self.request.url)[0]
        stream_name = re.findall('%3D%3D(.*)', self.request.url)[0]
        self.response.write('<h2>%s<h2>' % stream_name)
        stream_query = StreamModel.query(StreamModel.authorName==user, StreamModel.name==stream_name)
        #streams = stream_query.fetch()[0]
        pictures_query = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1 "+
                                     "ORDER BY uploadDate DESC", db.Key.from_path('StreamModel', stream_name))
        index = 0;
        for picture in pictures_query:
            if index==0:
                self.response.write('<tr>')
            self.response.write(PICTURE_ENTRY_TEMPLATE % picture.key())
            if index==5:
                self.response.write('</tr>')
            else:
                index += 1
        returnURL = urllib.urlencode({'stream':stream_name})
        self.response.write('<br><a href=%s> go back</a></br>' % returnURL)


app = webapp2.WSGIApplication([
    ('/showmore.*', ShowMore),
    ('/stream.*', ViewSingle),
    ('/upload', Upload),
    ('/pic.*', ViewPictureHandler)
], debug=True)


#
