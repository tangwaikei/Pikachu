from Management.models import Action
from httprunner.parser import is_var_or_func_exist


def action(action_id):
    a_action = Action.objects.get(id=action_id)
    action_type = a_action.type
    action = a_action.action
    if action_type == 1:
        #sql
        return '${execute_sql($action)}'
    elif action_type == 2:
        #等待时间
        return '${wait_some_time($action)}'
    elif action_type == 3:
        #执行http请求
        return '${http_request($action)}'
    elif action_type == 4:
        #执行测试用例
        pass
    elif action_type == 5:
        #执行脚本方法
        if is_var_or_func_exist(action):
            return action
        else:
            RuntimeError('函数不存在')