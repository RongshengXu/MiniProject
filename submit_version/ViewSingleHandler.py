from Stream import PictureModel, StreamModel, CountViewModel
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.ext import blobstore

import webapp2
import re
import urllib

NUM_PICTURE_PER_STREAM = 4

VIEW_SINGLE_PAGE_TEMPLATE = """\
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
    <h3>View A Single stream</h3>
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

SUBSCRIBE_ENTRY_TEMPLATE = """\
<form action="%s" method="post">
    <input type="submit" value="Subscribe">
</form>
"""

UNSUBSCRIBE_ENTRY_TEMPLATE = """\
<form action="%s" method="post">
    <input type="submit" value="Unsubscribe">
</form>
"""

MORE_ENTRY_TEMPLATE = """\
<form action="%s" ,method="post">
    <input type="submit" value="More Pictures">
</form>
<hr>
"""

PICTURE_ENTRY_TEMPLATE = """\
<td><img src="pic?pic_id=%s"></img></td>
"""

class ViewSingle(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        stream_name = re.findall('%3D(.*)', self.request.url)[0]
        #self.response.write(stream_name)
        self.response.write(VIEW_SINGLE_PAGE_TEMPLATE)
        self.response.write('<h3>%s</h3>' % stream_name)
        # stream_query = StreamModel.query(StreamModel.name==stream_name, StreamModel.author==user)
        stream_query = StreamModel.query(StreamModel.name==stream_name)
        stream = stream_query.fetch()[0]

        self.response.write('<table style="width:100%"><tr>')
        picture_query = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1 ORDER BY uploadDate DESC LIMIT 5",
                                  db.Key.from_path('StreamModel', stream_name))
        index = 0
        for picture in picture_query:
            if (index < NUM_PICTURE_PER_STREAM):
                index += 1
                self.response.write(PICTURE_ENTRY_TEMPLATE % picture.key())
        self.response.write('</tr></table>')
        morePictureURL = urllib.urlencode({'showmore':user.nickname()+"=="+stream_name})
        self.response.write(MORE_ENTRY_TEMPLATE % morePictureURL)
        if (stream.author == user):
            self.response.write(UPLOAD_ENTRY_TEMPLATE)
        else:
            countView_query = CountViewModel.query(CountViewModel.name==stream_name).fetch()
            if len(countView_query)>0:
                countView = countView_query[0]
                countView.count = countView.count + 1
                countView.total = countView.total + 1
                countView.put()
            url = urllib.urlencode({'subscribe':stream_name})

            if user.nickname() in stream.subscribers:
                url = urllib.urlencode({'unsubscribesingle':stream_name})
                self.response.write(UNSUBSCRIBE_ENTRY_TEMPLATE % url)
            else:
                url = urllib.urlencode({'subscribe':stream_name})
                self.response.write(SUBSCRIBE_ENTRY_TEMPLATE % url)

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
            stream_query = StreamModel.query(StreamModel.name==stream_name)
            stream = stream_query.fetch()[0]
            if (stream.author == users.get_current_user()):
                stream.totalPicture = stream.totalPicture + 1
                user_picture = PictureModel(parent = db.Key.from_path('StreamModel', stream_name))
                user_picture.id = str(stream.totalPicture)
                picture = images.resize(picture, 320, 400)
                user_picture.picture = db.Blob(picture)
                user_picture.put()
                stream.lastUpdated = user_picture.uploadDate
                stream.put()
        self.redirect(returnURL)

class ShowMore(webapp2.RequestHandler):
    def get(self):
        user = re.findall('%3D(.*)%3D%3D', self.request.url)[0]
        stream_name = re.findall('%3D%3D(.*)', self.request.url)[0]
        self.response.write('<h2>%s<h2>' % stream_name)
        stream_query = StreamModel.query(StreamModel.name==stream_name)
        stream = stream_query.fetch()[0]
        pictures_query = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1 "+
                                     "ORDER BY uploadDate DESC", db.Key.from_path('StreamModel', stream_name))
        index = 0
        for picture in pictures_query:
            if index==0:
                self.response.write('<tr>')
            self.response.write(PICTURE_ENTRY_TEMPLATE % picture.key())

            if index==5:
                self.response.write('</tr>')
                index=0
            else:
                index += 1
        if (stream.author == users.get_current_user()):
            pass
        else:
            countView_query = CountViewModel.query(CountViewModel.name==stream_name).fetch()
            if len(countView_query)>0:
                countView = countView_query[0]
                countView.count = countView.count - 1
                countView.total = countView.total - 1
                countView.put()
        returnURL = urllib.urlencode({'stream':stream_name})
        self.response.write('<br><a href=%s> go back</a></br>' % returnURL)


class clearViewCount(webapp2.RequestHandler):
    def get(self):
        countView = CountViewModel.query().fetch()
        if len(countView)>0:
            for count in countView:
                count.count = 0
                count.put()

class Subscirbe(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        self.response.write(self.request.url)
        stream_name = re.findall("subscribe%3D(.*)",self.request.url)[0]
        self.response.write(stream_name)
        stream_query = StreamModel.query(StreamModel.name==stream_name).fetch()
        if len(stream_query)>0:
            stream = stream_query[0]
            stream.subscribers.append(users.get_current_user().nickname())
            stream.put()
        self.redirect(returnURL)

class UnsubscribeSingle(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        self.response.write(self.request.url)
        stream_name = re.findall("unsubscribesingle%3D(.*)",self.request.url)[0]
        self.response.write(stream_name)
        stream_query = StreamModel.query(StreamModel.name==stream_name).fetch()
        if len(stream_query)>0:
            stream = stream_query[0]
            stream.subscribers.remove(users.get_current_user().nickname())
            stream.put()
        self.redirect(returnURL)

app = webapp2.WSGIApplication([
    ('/showmore.*', ShowMore),
    ('/stream.*', ViewSingle),
    ('/upload', Upload),
    ('/pic.*', ViewPictureHandler),
    ('/subscribe.*', Subscirbe),
    ('/clearviewcount', clearViewCount),
    ('/unsubscribesingle.*', UnsubscribeSingle)
], debug=True)
