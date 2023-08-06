# -*- coding: utf-8 -*-

from django.conf import settings

FOOLISH_AUTH_USER_SAVED = getattr(settings, 'FOOLISH_AUTH_USER_SAVED', False)
FOOLISH_AUTH_CREATE_USER = getattr(settings, 'FOOLISH_AUTH_CREATE_USER', True)
