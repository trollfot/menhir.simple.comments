from zope.i18nmessageid import MessageFactory
_d_ = MessageFactory("dolmen")
_ = MessageFactory("menhir.simple.comments")

from menhir.simple.comments.interfaces import IComment, IComments, ICommentable
from menhir.simple.comments.comment import Comment
from menhir.simple.comments.container import Commenting
