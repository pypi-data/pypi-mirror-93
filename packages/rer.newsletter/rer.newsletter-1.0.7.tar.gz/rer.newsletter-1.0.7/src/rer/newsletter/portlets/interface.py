# -*- coding: utf-8 -*-
from plone import api
from plone import schema
from rer.newsletter import _
from rer.newsletter.content.channel import Channel
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import re


@provider(IContextAwareDefaultFactory)
def getDefaultChannel(context):
    for obj in context.aq_chain:
        if isinstance(obj, Channel):
            return api.content.get_uuid(obj=obj)


class IPortletTileSchema(Interface):
    header = schema.TextLine(
        title=_(u'title_portlet_header', default=u'Header'),
        description=_(u'description_portlet_header',
                      default=u'Title of the rendered portlet'),
        constraint=re.compile('[^\s]').match,
        required=False)

    # link_to_archive = schema.ASCIILine(
    #     title=_(u'title_portlet_link', default=u'Details link'),
    #     description=_(
    #         u'description_portlet_link',
    #         default=u'If given, the header and footer will link to this URL.'
    #     ),
    #     required=False)

    css_class = schema.TextLine(
        title=_(u'title_css_portlet_class', default=u'Portlet class'),
        description=_(u'description_css_portlet_class',
                      default=u'CSS class to add at the portlet'),
        required=False
    )

    newsletter = schema.Choice(
        title=_(u'title_newsletter', default=u'Newsletter'),
        description=_(u'description_newsletter',
                      default=u'Newsletters'),
        vocabulary='rer.newsletter.subscribablenewsletter.vocabulary',
        defaultFactory=getDefaultChannel,
        required=False
    )
