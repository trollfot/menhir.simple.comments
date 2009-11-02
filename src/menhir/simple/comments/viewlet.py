# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface, directlyProvides
from zope.component import getMultiAdapter, getAdapter
from dolmen.app.layout import master, IDisplayView
from dolmen.app.authentication import IUserDirectory
from menhir.simple.comments import IComments, ICommentable
from zope.traversing.browser import absoluteURL

from zeam.utils.batch import batch
from zeam.utils.batch.interfaces import IBatching

grok.templatedir('templates')


def prepare_comments(container, keys, request):
    """This useful function returns a list of dicts, representing comments
    from a list of keys, present in the given container.
    """
    def author_name(author):
        """This inner function provides a formatted userid
        for zope-level users.
        """
        if author == "zope.anybody":
            return u"Anonymous"
        return author

    # We get a date formatter.
    formatter = request.locale.dates.getFormatter(
            u'dateTime', u'short', None, u'gregorian')
    
    for key in keys:
        comment = container[key]
        yield {'id': comment.__name__,
               'author': author_name(comment.author),
               'date': formatter.format(comment.date),
               'text': comment.text}


class Comments(grok.Viewlet):
    grok.order(20)
    grok.view(IDisplayView)
    grok.context(ICommentable)
    grok.viewletmanager(master.BelowBody)

    def form(self):
        form = getMultiAdapter(
            (self.context, self.request), name = u'comment'
            )
        form.update()
        form.updateForm()
        return form.render()

    def update(self):
        self.comments = []
        commenter = getAdapter(
            self.context, IComments, 'commenting.comments')
        commenter.__parent__ = self.context
        commenter.__name__ = u""
        
        self.avatar = self.view.application_url() + '/++avatar++'
   
        keys = list(reversed(commenter.keys()))
        batched_keys = batch(
            keys, count=6, name='comments', request=self.request)
        self.batch = getMultiAdapter(
            (self.view, batched_keys, self.request), IBatching)()

        self.comments = prepare_comments(
            commenter, batched_keys, self.request)
