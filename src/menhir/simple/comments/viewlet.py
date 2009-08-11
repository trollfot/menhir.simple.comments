# -*- coding: utf-8 -*-

import grok
from dolmen.app.layout import master, IDisplayView
from dolmen.app.authentication import IUserDirectory
from menhir.simple.comments import ICommentable
from zope.interface import Interface
from zope.component import getMultiAdapter, getUtility
from zope.annotation.interfaces import IAttributeAnnotatable
from dolmen.imaging import IImageMiniaturizer
from zope.app.publisher.browser.fileresource import FileResource
grok.templatedir('templates')


class Portrait(grok.View):
    grok.context(Interface)
               
    def render(self):
        uid = self.request.form.get('uid')
        if uid:
            users = getUtility(IUserDirectory)
            user = users.getUserByLogin(uid)
            if user is not None and user.portrait is not None:
                thumbs = IImageMiniaturizer(user)
                thumb = thumbs.retrieve_thumbnail(
                    "small", fieldname='portrait'
                    )
                if thumb:
                    return getMultiAdapter((thumb, self.request),
                                           name = "file_publish")()
        resource =  FileResource(self.static['unknown.gif'].context,
                                 self.request)
        resource.HEAD()
        return resource.GET()


class Comments(grok.Viewlet):
    grok.view(IDisplayView)
    grok.context(IAttributeAnnotatable)
    grok.viewletmanager(master.DolmenBelowBody)

    def update(self):
        commenter = ICommentable(self.context)
        self.show = False
        
        if commenter.enabled is True:
            self.baseurl = self.view.application_url()
            self.show = True
            self.form = getMultiAdapter((self.context, self.request),
                                        name = u'comment')
            self.form.update()
            self.form.updateForm()
            formatter = self.request.locale.dates.getFormatter(
                u'dateTime', u'medium', None, u'gregorian'
                )

            def author_name(author):
                if author == "zope.anybody":
                    return u"Anonymous"
                return author

            self.comments = [{'author': author_name(comment.author),
                              'date': formatter.format(comment.date),
                              'text': comment.text } for comment in
                             commenter.comments.values()]
            
