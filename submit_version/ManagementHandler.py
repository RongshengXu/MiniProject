from google.appengine.api import users

from Stream import StreamModel, PictureModel, CountViewModel
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import ndb
import webapp2

MANAGEMENT_PAGE_TEMPLATE ="""\
<!DOCTYPE html>
<html>
<body>
    <h1>Connex.us</h1>
    <table cellspacing="15">
        <tr>
            <td style="background-color:gray"><a href="manage">Manage</a></td>
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
            <th>|</th>
            <td><a href="%s">%s</a><td>
        </tr>
    </table>
    <hr size="5" />
    <h3>Streams I own</h3>
</body>
</html>
"""

STREAM_I_OWN_ENTRY = """\
<tr>
    <td><a href="%s">%s</a></td>
    <td>%s</td>
    <td>%s</td>
    <td><input type="checkbox" name="deleteStream", value="%s"></td>
</tr>
"""

STREAM_I_SUBSCRIBE_ENTRY = """\
<tr>
    <td><a href="%s">%s</a></td>
    <td>%s</td>
    <td>%s</td>
    <td><input type="checkbox" name="unSubscribe", value="%s"></td>
</tr>
"""

class ManagementPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if (user):
            url = users.create_logout_url(self.request.url)
            url_linktext = 'Logout'
            self.response.write(MANAGEMENT_PAGE_TEMPLATE % (url, url_linktext))

            stream_query = StreamModel.query(StreamModel.author==user).order(-StreamModel.createTime).fetch()
            self.response.write('<form action="/deletestream", method="post"><table border="1" style="width:100%">')
            self.response.write('<tr><td>Name</td><td>Last New Picture</td><td>Number of Pictures</td><td>Delete</td></tr>')
            if len(stream_query) > 0:
                for stream in stream_query:
                    self.response.write(STREAM_I_OWN_ENTRY % (stream.url, stream.name,
                                                              stream.lastUpdated, str(stream.totalPicture), stream.name))
            else:
                self.response.write('<tr><td align="center" colspan="4">No data available in table</td></tr>')

            self.response.write('</table>')
            self.response.write('<input type="submit" value ="Delete Checked"></form>')

            ################################################################################################################
            self.response.write('<h3>Streams I Subscribe to</h3>')
            stream_query = StreamModel.query().fetch()
            self.response.write('<form action="/unsubscribe", method="post"><table border="1" style="width:100%">')
            self.response.write('<tr><td>Name</td><td>Last New Picture</td><td>Number of Pictures</td><td>Unsubscribe</td></tr>')

            findone = False
            if len(stream_query) > 0:
                for stream in stream_query:
                    if user.nickname() in stream.subscribers:
                        findone = True
                        self.response.write(STREAM_I_SUBSCRIBE_ENTRY % (stream.url, stream.name,
                                                              stream.lastUpdated, str(stream.totalPicture), stream.name))
            if not findone:
                self.response.write('<tr><td align="center" colspan="4">No data available in table</td></tr>')

            self.response.write('</table>')
            self.response.write('<input type="submit" value ="Unsubscribe Checked"></form>')

        else:
            self.redirect('/')

class deleteStream(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        streams = self.request.get_all("deleteStream")
        if len(streams) > 0:
            countViews = CountViewModel.query(CountViewModel.name.IN(streams)).fetch()
            ndb.delete_multi(ndb.put_multi(countViews))
            stream_query = StreamModel.query(StreamModel.name.IN(streams), StreamModel.author==users.get_current_user())
            streams = stream_query.fetch()
            for stream in streams:
                pictures = db.GqlQuery("SELECT *FROM PictureModel WHERE ANCESTOR IS :1", db.Key.from_path('StreamModle',stream.name))
                db.delete(pictures)
            ndb.delete_multi(ndb.put_multi(streams))
        self.redirect(returnURL)

class unSubscribe(webapp2.RequestHandler):
    def post(self):
        returnURL = self.request.headers['Referer']
        streams = self.request.get_all("unSubscribe")

        if len(streams) > 0:
            stream_query = StreamModel.query(StreamModel.name.IN(streams))
            streams = stream_query.fetch()
            for stream in streams:
                stream.subscribers.remove(users.get_current_user().nickname())
                stream.put()

        self.redirect(returnURL)


app = webapp2.WSGIApplication([
    ('/manage', ManagementPage),
    ('/deletestream', deleteStream),
    ('/unsubscribe', unSubscribe),
], debug=True)
