# -*- coding: utf-8 -*-

import urlparse


def get_base_url(url):
    return '://'.join(urlparse.urlparse(url)[:2])
