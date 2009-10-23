# -*- coding: utf-8 -*-

import grokcore.component as grok

from persistent import Persistent
from BTrees.Length import Length
from zope.event import notify
from zope.app.container import contained
from zope.exceptions import DuplicationError
from menhir.simple.comments import IComments, ICommentable
from dolmen.storage import AnnotationStorage, IOBTreeStorage


class CommentStorage(IOBTreeStorage):
    """A container based on an IOBTree
    """
    def __delitem__(self, key):
        contained.uncontained(self[key], self, key)
        del self[key]

    def __setitem__(self, name, object):
        """Add the given object to the folder under the given name.
        """
        if not isinstance(name, int):
            raise TypeError("Name must be an integer rather than a %s" %
                            name.__class__.__name__)

        if self.__contains__(name):
            raise DuplicationError("key %r is already in use." % name)

        object, event = contained.containedEvent(object, self, name)
        IOBTreeStorage.__setitem__(self, name, object)

        if event:
            notify(event)
            contained.notifyContainerModified(self)


class Commenting(AnnotationStorage):
    grok.context(ICommentable)
    grok.provides(IComments)
    grok.name('commenting.comments')
    
    _factory = CommentStorage

    def insert(self, comment):
        tries = 0
        try:
            name = self.storage.maxKey() + 1
        except ValueError:
            name = 1
        inserted = False
        while inserted is False:
            if tries > 10:
                break
            try:
                self[name] = comment
                inserted = True
            except DuplicationError:
                name += 1
                tries += 1

        if inserted is True:
            return self[name]
        return None
