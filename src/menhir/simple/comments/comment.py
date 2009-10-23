# -*- coding: utf-8 -*-

import grok
from zope.component import getMultiAdapter
from zope.traversing.browser import absoluteurl
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.dublincore.property import DCProperty
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema.fieldproperty import FieldProperty
from menhir.simple.comments import IComment


class Comment(grok.Model):
    """A simple IComment implementation.
    """ 
    grok.implements(IComment)

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


class CommentURL(absoluteurl.AbsoluteURL, grok.MultiAdapter):
    grok.name('absolute_url')
    grok.adapts(IComment, IHTTPRequest)
    grok.provides(IAbsoluteURL)

    def __str__(self):
        context = self.context
        request = self.request

        import pdb
        pdb.set_trace()

        container = getattr(context, '__parent__', None)
        name = context.__name__
        url = absoluteurl.absoluteURL(container, request)
        return url + name
