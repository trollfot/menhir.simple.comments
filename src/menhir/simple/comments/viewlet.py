# -*- coding: utf-8 -*-

import grok
from dolmen.app.layout import master, IDisplayView
from menhir.simple.comments import ICommentable
from zope.component import getMultiAdapter
from zope.annotation.interfaces import IAttributeAnnotatable

grok.templatedir('templates')


class Comments(grok.Viewlet):
    grok.view(IDisplayView)
    grok.context(IAttributeAnnotatable)
    grok.viewletmanager(master.DolmenBelowBody)

    def update(self):
        commenter = ICommentable(self.context)
        self.show = False
        if commenter.enabled is True:
            self.show = True
            self.comments = commenter.comments.values()
            self.form = getMultiAdapter((self.context, self.request),
                                        name = u'comment')
            self.form.update()
            self.form.updateForm()
