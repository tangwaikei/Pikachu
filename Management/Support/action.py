from Management.models import Action
from django.db import connection
from Management.Support.util import is_number, http_request
import time


def action(action_id):
    a_action = Action.objects.get(id=action_id)
    action_type = a_action.type
    action = a_action.action
    if action_type == 1:
        #sql
        try:
            if isinstance(action, str):
                #判断是否sql
                cursor = connection.cursor()
                cursor.execute(action)
        except (TypeError) as err:
            print(err)
    elif action_type == 2:
        #等待时间
        if is_number(action):
            time.sleep(action)
        else:
            raise RuntimeError('等待时间非数字')
    elif action_type == 3:
        #执行http请求
        http_request(action)
    elif action_type == 4:
        #执行测试用例
        pass
    elif action_type == 5:
        #执行脚本方法
        pass