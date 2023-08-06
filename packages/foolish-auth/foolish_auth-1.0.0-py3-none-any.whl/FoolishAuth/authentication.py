# -*- coding: utf-8 -*-
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .settings import *


class FoolishAuthentication(TokenAuthentication):
    """
    只是简单的认可请求头中携带的用户信息，然后创建一个不保存的零时用户。
    此APP只能用于带有认证功能的API网关背后，用于简化系统内部的用户认证。
    """

    keyword = 'Foolish'

    def authenticate_credentials(self, key):
        user_model = get_user_model()

        if FOOLISH_AUTH_USER_SAVED:
            try:
                user = user_model.object.get(username=key)
            except user_model.DoseNotExist:
                if FOOLISH_AUTH_CREATE_USER:
                    user = user_model.object.create(username=key)
                else:
                    raise AuthenticationFailed(_('User inactive or deleted.'))
        else:
            user = user_model(username=key)

        return user, key

