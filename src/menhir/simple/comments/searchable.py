# -*- coding: utf-8 -*-

import grokcore.component as grok
from menhir.simple.comments import IComment
from zope.index.text.interfaces import ISearchableText


class SearchableTextDocument(grok.Adapter):
    grok.context(IComment)
    grok.implements(ISearchableText)

    def getSearchableText(self):
        return self.context.text
