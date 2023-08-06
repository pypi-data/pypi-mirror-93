# -*- coding: utf-8 -*-
import hashlib
import random
import string
import time
from abc import abstractmethod
from typing import Optional

from flask import request
from pydantic import BaseModel, Field

from easi_py_common.core.error import ServiceException


class Sign2Service:
    def __init__(self, app_key: str, app_secret: str, salt: str = '&'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.salt = salt

    def __is_int(self, s):
        try:
            int(s)
            return True
        except Exception:
            pass
        return False

    def __sign(self, url: str, method: str, body_str: str, timestamp: str, nonce: str) -> str:
        signs = [self.app_key, self.app_secret, timestamp, nonce, method, url, body_str]
        signs = sorted(signs)
        sg = self.salt.join(signs)

        h = hashlib.md5()
        h.update(sg.encode("utf8"))
        sign = h.hexdigest()
        return sign.upper()

    def sign(self, url: str, method: str, body_str: str = '') -> (str, str, str):
        timestamp = str(int(time.time() * 1000))
        nonce = ''.join(random.sample(string.digits + string.ascii_letters, 32))
        sign = self.__sign(url, method, body_str, timestamp, nonce)

        return timestamp, nonce, sign

    def valid(self, app_key: str, url: str, method: str, body_str: str, timestamp: str, nonce: str, sign: str) -> bool:
        if not app_key or app_key != self.app_key:
            return False
        if not nonce or len(nonce) < 16:
            return False
        if not timestamp or not self.__is_int(timestamp):
            return False
        if not sign:
            return False

        generate_sign = self.__sign(url, method, body_str, timestamp, nonce)
        return generate_sign == str(sign).upper()


class AppInfo(BaseModel):
    app_key: str = Field(..., description='app_key')
    app_secret: str = Field(..., description='app_secret')
    self_info: Optional[object] = Field(description='self_info')


class AppInfoService:
    @abstractmethod
    def get_app_info(self, app_key: str) -> AppInfo: pass


class AppSignValidService:
    def __init__(self, app_info_service: AppInfoService, salt: str = '&',
                 header_app_key: str = 'app_key',
                 header_timestamp: str = 'timestamp',
                 header_nonce: str = 'nonce',
                 header_sign: str = 'sign'):

        self.app_info_service = app_info_service
        self.salt = salt
        self.header_app_key = header_app_key
        self.header_timestamp = header_timestamp
        self.header_nonce = header_nonce
        self.header_nonce = header_nonce
        self.header_sign = header_sign

    def __get_header_value(self, name):
        return request.headers[name] if name in request.headers else None

    def __get_url(self):
        url = request.full_path
        index = url.index("?")
        if index != -1:
            if len(url) - index == 1:
                url = url[0:index]
        return url

    def valid(self):
        app_key = self.__get_header_value(self.header_app_key)
        timestamp = self.__get_header_value(self.header_timestamp)
        nonce = self.__get_header_value(self.header_nonce)
        sign = self.__get_header_value(self.header_sign)
        request_data = request.get_data().decode('utf-8')
        url = self.__get_url()

        app_info = self.app_info_service.get_app_info(app_key)
        sign2_service = Sign2Service(app_info.app_key, app_info.app_secret, self.salt)
        if not sign2_service.valid(app_key=app_key, url=url, method=request.method.upper(),
                                   body_str=request_data, timestamp=timestamp, nonce=nonce, sign=sign):
            raise ServiceException(code=400, msg=u"invalid sign")

        return app_info.self_info
