# !/usr/bin/env python
# coding: utf-8
# @Time         : 2021/2/1 9:21
# @File         : config.py
# @Desc         : ---
# @Software     : PyCharm
# @Author       : 支立伟
# @Email        : ligocz@dingtalk.com


# redis缓存的key的分隔符
CACHE_KEY_SEPARATOR = '|'

# 无效的jwt的缓存时长，秒
INVALID_JWT_TTL: int = 3600 * 24 * 15
