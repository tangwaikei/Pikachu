import json
import requests
import io, yaml

def dict_fetchone(cursor):

    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def is_number(string):
    is_string_number = True
    try:
        if str.lower(string) in ['nan', 'inf']:
            is_string_number = False
        else:
            num = float(string)
    except ValueError:
        is_string_number = False
    return is_string_number


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
    if res:
        return res.status_code == 200


def testcase_to_yml(path, yaml_dict):
    with io.open(path, 'a', encoding='utf-8') as stream:
        yaml.dump(yaml_dict, stream, encoding='utf-8')


