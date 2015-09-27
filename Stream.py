__author__ = 'rongshengxu'

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

class StreamModel(ndb.Model):
    """ stream model
    """
    name = ndb.StringProperty()
    author = ndb.UserProperty()
    authorName = ndb.StringProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    lastUpdated = ndb.DateTimeProperty(auto_now=True)
    url = ndb.StringProperty()
    tag = ndb.StringProperty(repeated=True)
    subscribers = ndb.StringProperty(repeated=True)
    message = ndb.StringProperty()
    coverpageURL = ndb.StringProperty()
    totalPicture = ndb.IntegerProperty()

class PictureModel(db.Model):
    """ picture model
    """
    picture = db.BlobProperty()
    id = db.StringProperty()
    uploadDate = db.DateTimeProperty(auto_now_add=True)