# -*- coding: utf-8 -*-

import grok
import dolmen.forms.base as form
from dolmen.app.layout import models

from zope.event import notify
from zope.component import getAdapter
from zope.lifecycleevent import ObjectCreatedEvent

from menhir.simple.comments import Comment, _
from menhir.simple.comments import IComment, IComments, ICommentable


class AddComment(form.PageAddForm, models.ApplicationAwareView):
    grok.name('comment')
    grok.context(ICommentable)

    fields = form.Fields(IComment).select('text')
    form_name = _(u"Add a new comment")

    def update(self):
        self.comments = getAdapter(
            self.context, IComments, name='commenting.comments')

    def create(self, data):
        obj = Comment()
        form.apply_data_event(self.fields, obj, data)
        return obj

    def add(self, comment):
        added = self.comments.insert(comment)
        if added is None:
            self.flash(_(u"Your comment couldn't be added. Please retry."))
        else:
            self.flash(_(u"Your comment has been added."))
        return added
        
    def nextURL(self):
        return self.url(self.context)
