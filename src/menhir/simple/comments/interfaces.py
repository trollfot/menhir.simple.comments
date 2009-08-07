# -*- coding: utf-8 -*-

from menhir.simple.comments import _
from zope.schema import Object, Bool, Text
from zope.interface import Interface, Attribute
from zope.container.constraints import contains
from zope.container.interfaces import IContainer, IContained


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


class ICommentable(Interface):
    """Defines a commentable object.
    """
    enabled = Bool(
        title = _(u'Enable commenting'),
        default = True,
        required = False,
        )

    comments = Object(
        title = _(u'Commenting container'),
        required = True,
        schema = IComments
        )

    def add(comment):
        """Add a comment to the commenting container.
        """
