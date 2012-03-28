# -*- coding: utf-8 -*-

from tastypie.api import Api
from resources import UserResource, WebsiteResource, FeedResource, EntryResource, VisistedResource, SubscriptionResource


# Create REST API:
api_v1 = Api(api_name='v1')
api_v1.register(UserResource())
api_v1.register(WebsiteResource())
api_v1.register(FeedResource())
api_v1.register(EntryResource())
api_v1.register(VisistedResource())
api_v1.register(SubscriptionResource())
