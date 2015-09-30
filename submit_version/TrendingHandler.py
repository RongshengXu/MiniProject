from Stream import StreamModel
from Stream import CountModel, CountViewModel
from google.appengine.api import users
from google.appengine.api import mail
import webapp2

SERVICE_DOMAIN="sacred-highway-108321"
MAILBOX=".appspotmail.com"
EMAIL_SENDER="Connexus"

TRENDING_PAGE_TEMPLATE = """\
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
</body>
</html>
"""

freq_dict = {0: 'No reports', 1:'Every 5 minutes', 12:'Every 1 hour', 288:'Every day'}

DEFAULT_TRENDING_MESSAGE = "Trending update"
DEFAULT_TRENDING_SUBJECT = "Trending digest from "
TAEmail = "xurongsheng2010@gmail.com"

STREAM_ENTRY_TEMPLATE = """\
<td>
    <div style = "position:relative;">
        <a href="%s">
            <img src="%s" height="150" width="150"></img>
            <div style = "position: relative; left:65px; top:0px">%s</div>
        </a>
        <div style = "position: relative; left:10px; top:5px">%s</div>
    </div>
</td>
"""

TRENDING_REPORT_TEMPLATE = """\
<h3>Email trending report</h3>
<form action="/update" method="post">
    <input type="radio" name="frequency" value="No reports" checked>No reports</input><br>
    <input type="radio" name="frequency" value="Every 5 minutes">Every 5 minutes</input><br>
    <input type="radio" name="frequency" value="Every 1 hour">Every 1 hour</input><br>
    <input type="radio" name="frequency" value="Every day">Every day</input><br>
    <input type="submit" value="Update rate">
</form>
<hr>
"""

class Trending(webapp2.RequestHandler):
    def get(self):
        self.response.write(TRENDING_PAGE_TEMPLATE)
        countView_query = CountViewModel.query().order(-CountViewModel.count).fetch()
        index = 0
        self.response.write('<table border="0" style="width:100%">')
        if len(countView_query)> 0:
            for view in countView_query:
                if index < 3:
                    index += 1
                    stream_query = StreamModel.query(StreamModel.name == view.name).fetch()
                    if len(stream_query)>0:
                        stream = stream_query[0]
                        self.response.write(STREAM_ENTRY_TEMPLATE % (stream.url, stream.coverpageURL, stream.name, str(view.count) + " views in past hour"))

        self.response.write('</table><hr>')

        self.response.write(TRENDING_REPORT_TEMPLATE)
        count_query = CountModel.query(CountModel.name=="Trending").fetch()
        if len(count_query)==0:
            count = CountModel(name="Trending", count=0, freq=0)
            self.response.write( "Present frequency: No reports")
            count.put()
        else:
            count = count_query[0]
            self.response.write("Present frequency: "+freq_dict[count.freq])

class Update(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        returnURL = self.request.headers['Referer']
        frequency = self.request.get("frequency")
        count_query = CountModel.query(CountModel.name=="Trending").fetch()
        if len(count_query)>0:
            count = count_query[0]
            if frequency == "No reports":
                count.f = 0
                count.freq = 0
            elif frequency == "Every 5 minutes":
                count.f = 1
                count.freq = 1
            elif frequency == "Every 1 hour":
                count.f = 12
                count.freq = 12
            elif frequency == "Every day":
                count.f = 288
                count.freq = 288
            count.put()
        self.redirect(returnURL)

class CountDown(webapp2.RequestHandler):
    def get(self):
        sender = EMAIL_SENDER + "@"+SERVICE_DOMAIN+MAILBOX
        cd_query = CountModel.query(CountModel.name=="Trending").fetch()
        if (len(cd_query)>0):
            cd = cd_query[0]
            if cd.freq != 0:
                cd.count = cd.count + 1
                if (cd.count == cd.freq):
                    cd.count = 0
                    subject = DEFAULT_TRENDING_SUBJECT + EMAIL_SENDER
                    mail.send_mail(sender=sender, to=TAEmail, subject=subject, body=DEFAULT_TRENDING_MESSAGE)
                    mail.send_mail(sender=sender, to="xurongsheng2010@gmail.com", subject=subject, body=DEFAULT_TRENDING_MESSAGE)
                    mail.send_mail(sender=sender, to="yangxuanemail@gmail.com", subject=subject, body=DEFAULT_TRENDING_MESSAGE)
                cd.put()
        #else:
            #mail.send_mail(sender="test@example.com", to="xurongsheng2010@gmail.com", subject="test", body=DEFAULT_TRENDING_MESSAGE)


app = webapp2.WSGIApplication([
    ('/trending', Trending),
    ('/update', Update),
    ('/countdown', CountDown)
], debug=True)

