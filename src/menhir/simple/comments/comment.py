# -*- coding: utf-8 -*-

from grok import Model
from zope.interface import implements
from zope.dublincore.property import DCProperty
from zope.schema.fieldproperty import FieldProperty
from menhir.simple.comments import IComment


class Comment(Model):
    """A simple IComment implementation.
    """ 
    implements(IComment)

    _id = None
    date = DCProperty('created')
    author = DCProperty('creators')
    text = FieldProperty(IComment['text'])

    @apply
    def __name__():
        def get(self):
            return unicode(str(self._id))
        def set(self, id):
            self._id = int(id)
        return property(get, set)
