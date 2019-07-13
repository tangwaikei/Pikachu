# encoding: utf-8
import json
import requests
from django.db import connection
import time
from Management.Support.util import is_number, isset_var


def http_request(action):
    extra = {}
    action_arr = json.loads(action)
    url = action_arr['url']
    method = str.lower(action_arr['method'])
    has_timeout = False
    if 'headers' in action_arr:
        extra['headers'] = action_arr['headers']
    if 'files'in action_arr:
        extra['files'] = action_arr['files']
    if 'data'in action_arr:
        extra['data'] = action_arr['data']#元组列表，字典，json
    if 'cookie' in action_arr:
        cookie = action_arr['cookie']
        extra['cookie'] = cookie
    if 'allow_redirects' in action_arr:
        allow_redirects = action_arr['allow_redirects']
        extra['allow_redirects'] = allow_redirects
    if 'verify' in action_arr:
        extra['verify'] = action_arr['verify']
    if 'stream' in action_arr:
        extra['stream'] = action_arr['stream']
    if 'timeout' in action_arr:
        has_timeout = True
        extra['timeout'] = action_arr['timeout']
    if not has_timeout:
        extra['timeout'] = None
        #远端服务器很慢，你可以让 Request 永远等待
    if method not in ['get', 'post', 'delete', 'put', 'options', 'head', 'patch']:
        return False#非法方法
    if len(extra) == 0:
        if method == 'get':
            res = requests.get(url)
        elif method == 'post':
            res = requests.post(url)
        else:
            pass
    else:
        if method == 'get':
            res = requests.get(url, extra)
        elif method == 'post':
            res = requests.post(url, extra)
        else:
            pass
    if isset_var(res):
        return res.status_code == 200


def execute_sql(action):
    try:
        if isinstance(action, str):
            # 判断是否sql
            cursor = connection.cursor()
            cursor.execute(action)
    except (TypeError) as err:
        print(err)


def wait_some_time(action):
    if is_number(action):
        time.sleep(action)
    else:
        raise RuntimeError('等待时间非数字')





