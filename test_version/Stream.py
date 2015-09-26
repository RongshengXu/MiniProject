__author__ = 'rongshengxu'

from google.appengine.ext import ndb

class StreamModel(ndb.Model):
    """ stream model
    """
    name = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty(indexed=False)
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    tag = ndb.StringProperty(repeated=True)
    subscribers = ndb.StringProperty(repeated=True)
    message = ndb.StringProperty(indexed=True)
    coverpageURL = ndb.StringProperty()
