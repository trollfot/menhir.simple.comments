# -*- coding: utf-8 -*-

from persistent import Persistent
from BTrees.Length import Length
from BTrees.IOBTree import IOBTree
from zope.event import notify
from zope.interface import implements
from zope.app.container import contained
from zope.cachedescriptors.property import Lazy
from menhir.simple.comments import IComments


class CommentingFolder(Persistent, contained.Contained):
    implements(IComments)
    
    def __init__(self):
        self.data = IOBTree()
        self.__len = Length()
        self.__internal_id = 0

    def __contains__(self, key):
        return key in self.data

    @Lazy
    def _BTreeContainer__len(self):
        l = Length()
        ol = len(self._SampleContainer__data)
        if ol > 0:
            l.change(ol)
        self._p_changed = True
        return l

    def __len__(self):
        return self.__len()

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def next_id(self):
        return self.__internal_id + 1

    def __setitem__(self, name, object):
        """Add the given object to the folder under the given name.
        """
        if not isinstance(name, int):
            raise TypeError("Name must be an integer rather than a %s" %
                            name.__class__.__name__)

        if name in self.data:
            raise KeyError("id '%s' is already in use" % name)

        if name is not self.next_id():
            raise KeyError("id '%s' is not a direct incrementation" % name)

        object, event = contained.containedEvent(object, self, name)
        l = self.__len
        IOBTree.__setitem__(self.data, name, object)
        self.__internal_id += 1
        l.change(1)

        if event:
            notify(event)
            contained.notifyContainerModified(self)

    def __delitem__(self, key):
        l = self.__len
        contained.uncontained(self.data[key], self, key)
        del self.data[key]
        l.change(-1)

    has_key = __contains__

    def items(self, key=None):
        return self.data.items(key)

    def keys(self, key=None):
        return self.data.keys(key)

    def values(self, key=None):
        return self.data.values(key)
