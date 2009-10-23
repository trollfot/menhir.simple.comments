# -*- coding: utf-8 -*-

from zope.schema import Text
from zope.interface import Interface, Attribute
from zope.app.container.constraints import contains
from zope.app.container.interfaces import IContainer, IContained
from menhir.simple.comments import _


class ICommentable(Interface):
    """Marker interface for the items that can be commented.
    """


class IComment(IContained):
    """A comment associated to an object.
    """
    date = Attribute("Date of the comment posting")
    author = Attribute("Username of the comment author")
    
    text = Text(
        title = _(u'Comment body text'),
        required = True,
        default = u'',
        )


class IComments(IContainer):
    """A commenting container containing all the comments for an object.
    """
    contains(IComment)

    def insert(comment):
        """Adds a comment.
        """
