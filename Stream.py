__author__ = 'rongshengxu'

from google.appengine.api import users
from google.appengine.api import ndb

class StreamModel(ndb.Model):
    """ stream model
    """
    name = ndb.StringProperperty(indexed=False)
    author = ndb.StringProperperty(indexed=False)
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    tag = ndb.StringProperperty(repeated=True)
    subscribers = ndb.StringProperperty(repeated=True)
    message = ndb.StringProperperty(indexed=True)
    coverpageURL = ndb.StringProperperty()
