# -*- coding: utf-8 -*-

from z3c.form import field, form, button, widget
import megrok.z3cform

import grokcore.formlib as grok
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.annotation.interfaces import IAttributeAnnotatable
from menhir.simple.comments import IComment, Comment, ICommentable
from menhir.simple.comments import _, _d_ as __


class AddComment(megrok.z3cform.PageAddForm):
    grok.name('comment')
    grok.context(IAttributeAnnotatable)

    fields = field.Fields(IComment).omit('__parent__', '__name__')
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
