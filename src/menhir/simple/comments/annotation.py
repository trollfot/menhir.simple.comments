# -*- coding: utf-8 -*-

import grokcore.annotation as grok
import menhir.simple.comments as menhir
from zope.schema.fieldproperty import FieldProperty
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.container.contained import contained


class Commenting(grok.Annotation):
    grok.name('menhir.simple.comments')
    grok.context(IAttributeAnnotatable)
    grok.implements(menhir.ICommentable)
    
    enabled = FieldProperty(menhir.ICommentable['enabled'])

    def __init__(self):
        self._comments = menhir.CommentingFolder()

    @property
    def comments(self):
        return self._comments

    def add(self, comment):
        cid = self.comments.next_id()
        self.comments[cid] = comment
