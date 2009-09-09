# -*- coding: utf-8 -*-

import grokcore.formlib as grok
import dolmen.forms.base as form

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.annotation.interfaces import IAttributeAnnotatable
from menhir.simple.comments import IComment, Comment, ICommentable, _


class AddComment(form.PageAddForm):
    grok.name('comment')
    grok.context(IAttributeAnnotatable)

    fields = form.Fields(IComment).omit('__parent__', '__name__')
    form_name = _(u"Add a new comment")

    def create(self, data):
        obj = Comment()
        notify(ObjectCreatedEvent(obj))
        form.applyChanges(self, obj, data)
        return obj

    def add(self, comment):
        return self.comments.add(comment)

    def update(self):
        self.comments = ICommentable(self.context, None)
        if self.comments is None or self.comments.enabled is False:
            self.flash(_(u'Commenting is not allowed'))
            self.redirect(absoluteURL(self.context, self.request))

    def nextURL(self):
        return self.url(self.context)
