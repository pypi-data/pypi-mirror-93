# coding: utf-8
# !/usr/bin/env python
# coding: utf-8
# @Time         : 2021/2/1 9:11
# @File         : user_jwt.py
# @Desc         : ---
# @Software     : PyCharm
# @Author       : 支立伟
# @Email        : ligocz@dingtalk.com


import json
from datetime import datetime, timedelta

from django.conf import settings
from jose import jwt
from passlib.context import CryptContext

from nhl_user_jwt.config import CACHE_KEY_SEPARATOR, INVALID_JWT_TTL

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def _gen_jwt_sub(user_id: int, app_user_id: int):
    return f'[{user_id}, {app_user_id}]'


def create_access_token(user_id: int, app_user_id: int, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": _gen_jwt_sub(user_id, app_user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_access_token(redis_pool, token: str):
    """
    jwt验签：成功后返回payload中的用户数据
    1.jwt是否能被正确解析
    2.是否在有效期
    3.用户是否被冻结或禁用

    :param redis_pool:
    :param token:
    :return:
    """

    # 解析payload
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
    except jwt.JWTError:
        # todo logger.debug(traceback.format_exc())
        return {'success': False}

    sub = json.loads(payload.get('sub'))
    exp = payload.get('exp')

    # 日期检测
    exp_datetime = datetime.fromtimestamp(float(exp))
    if exp_datetime <= datetime.utcnow():
        return {'success': False}

    # 是否被强制退出
    invalid_jwt_cache = InvalidJWTCache(redis_pool)
    if invalid_jwt_cache.get(*sub):
        return {'success': False}
    return {'success': True, 'data': {'sub': sub}}


class InvalidJWTCache:
    """
    强制退出：
    被冻结或禁用的用户，以jwt中的sub为key在redis中做标记，在进行jwt验签时，强制退出该用户。
    用户登录在前，冻结或禁用操作在后时有效。结合用户的最后登录时间使用
    """

    def __init__(self, redis_pool):
        self.redis_pool = redis_pool

    @staticmethod
    def _gen_cache_key(user_id, app_user_id):
        sub = _gen_jwt_sub(user_id, app_user_id)
        return CACHE_KEY_SEPARATOR.join(['INVALID_JWT', sub])

    def set(self, user_id: int, app_user_id: int):
        key = self._gen_cache_key(user_id, app_user_id)
        self.redis_pool.set(key, 1, expire=INVALID_JWT_TTL)
        return True

    def get(self, user_id: int, app_user_id: int) -> bool:
        key = self._gen_cache_key(user_id, app_user_id)
        val = self.redis_pool.get(key)
        return True if val else False

    def delete(self, user_id: int, app_user_id: int) -> bool:
        self.redis_pool.delete(self._gen_cache_key(user_id, app_user_id))
        return True

