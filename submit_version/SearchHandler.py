from Stream import StreamModel
from google.appengine.api import users
import webapp2
import re

SEARCH_PAGE_TEMPLATE = """\
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
            <td style="background-color:gray"><a href="search">Search</a></td>
            <th>|</th>
            <td><a href="trending">Trending</a></td>
            <th>|</th>
            <td><a href="social">Social</a></td>
        </tr>
    </table>
    <hr size="5" />
    <h3>Search Streams</h3>
    <form action="/searchresult" method="get">
        <input type="search" name="searchPattern" placeholder="I'm lucky"><br>
        <input type="submit" value="Search">
    </form>
</body>
</html>
"""

STREAM_ENTRY_TEMPLATE = """\
<td>
    <a href="%s">
        <div style = "position:relative;">
            <img src="%s" height="100" width="100"></img>
            <div style = "position: relative; left:0px; top:0px">%s</div>
        </div>
    </a>
</td>
"""

SEARCH_RESULT_PAGE = """\

"""

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.write(SEARCH_PAGE_TEMPLATE)

class SearchResult(webapp2.RequestHandler):
    def get(self):
        self.response.write(SEARCH_PAGE_TEMPLATE)
        returnURL = self.request.headers['Referer']
        #self.response.write(self.response.url)
        pattern = self.request.get("searchPattern")
        Name = []
        StreamName = []
        streams = StreamModel.query().fetch()
        for st in streams:
            Name.append(st.name)
        num = 0
        for name in Name:
            fi = re.findall(pattern, name)
            #self.response.write(name)
            #self.response.write(fi)
            if len(fi)>0:
                stream = StreamModel.query(StreamModel.name==name).fetch()[0]
                StreamName.append(name)
                if num==0:
                    self.response.write("<tr>")
                self.response.write(STREAM_ENTRY_TEMPLATE % (stream.url, stream.coverpageURL, stream.name))
                if num==3:
                    self.response.write("</tr>")
                    num = 0
                else:
                    num += 1
        #self.redirect(returnURL)

app = webapp2.WSGIApplication([
    ('/search', Search),
    ('/searchresult', SearchResult)
], debug=True)
