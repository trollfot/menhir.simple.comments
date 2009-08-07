"""
About
=====

Comments are simple objects that can be added on any annotable content.
They are stored in a special container and can be accessed easily.

Let's create a simple content and add comments on it.

  >>> import grok
  >>> class ContentType(grok.Model):
  ...   '''A very basic content type.
  ...   '''

  >>> from zope.annotation.interfaces import IAttributeAnnotatable
  >>> content = ContentType()
  >>> IAttributeAnnotatable.providedBy(content)
  True

Annotations
===========

In order to add and manage the comments, an adapter is available.
It provides a simple access to the key features. Let's have an overview :

  >>> from menhir.simple.comments import ICommentable
  >>> commenter = ICommentable(content, None)
  >>> commenter is not None
  True
  >>> commenter.enabled is True
  True
  >>> commenter.comments
  <menhir.simple.comments.container.CommentingFolder object at ...>
  >>> len(commenter.comments)
  0

As we can see below, the commenting system has created a namespace in the
object's annotations:

  >>> from zope.annotation.interfaces import IAnnotations
  >>> ann = IAnnotations(content)
  >>> ann.has_key('menhir.simple.comments')
  True

Adding
======

Let's now add a comment :

  >>> from menhir.simple.comments import Comment, IComment
  >>> opinion = Comment()
  >>> IComment.providedBy(opinion)
  True
  >>> opinion.text
  u''
  >>> opinion.date
  >>> opinion.author
  Traceback (most recent call last):
  ...
  IndexError: tuple index out of range

There error is due to the lack of metadata. The Comment metadata are based on
the Zope's dublincore implementation and rely on a succession of event. Let's
now reproduce what's going on with the zope machinery :

First, we create a principal :

  >>> import zope.security.management
  >>> import zope.security.interfaces
  >>> from zope import interface

  >>> class Principal(object):
  ...     interface.implements(zope.security.interfaces.IPrincipal)
  ...
  ...     def __init__(self, id, title, description):
  ...         self.id = id
  ...         self.title = title
  ...         self.description = description
  ...
  ...     def __repr__(self):
  ...         return '<User %r>' % self.id

  >>> conan = Principal('conan', 'Conan (the) Barbarian', 'main user')


Second, we initiate the participation:  

  >>> class Participation(object):
  ...     zope.interface.implements(
  ...         zope.security.interfaces.IParticipation,
  ...         zope.publisher.interfaces.IRequest)
  ...     interaction = principal = None
  ...
  ...     def __init__(self, principal):
  ...         self.principal = principal
  ...
  ...     def __repr__(self):
  ...         return '<Participation %r>' % self.principal

  >>> zope.security.management.endInteraction()
  >>> zope.security.management.newInteraction(Participation(conan))

Now, we have set a nice environnement. We can trigger our event.

  >>> from zope.event import notify
  >>> from zope.lifecycleevent import ObjectCreatedEvent
  >>> notify(ObjectCreatedEvent(opinion))
  >>> opinion.date
  datetime.datetime(...)
  >>> opinion.author
  u'conan'

Finally, we can add it to the content:

  >>> commenter.add(opinion)
  >>> len(commenter.comments)
  1
  >>> [key for key in commenter.comments.keys()]
  [1]

Lovely. Our comment has now been added. We can easily get it with :

  >>> comment = commenter.comments.get(1)
  >>> comment
  <menhir.simple.comments.comment.Comment object at ...>
  >>> comment.__name__
  1

We can, also, delete it :

  >>> del commenter.comments[1]
  >>> commenter.comments.get(1) is None
  True
  >>> len(commenter.comments)
  0

The commenter is empty, but, out id counter is not reseted.

  >>> commenter.add(opinion)
  >>> [key for key in commenter.comments.keys()]
  [2]

"""
