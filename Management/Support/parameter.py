import os
from django.db import connection
import django
import json
from Management.models import Parameter, ParameterSql
from Management.Support.util import dict_fetchone
from httprunner.parser import is_var_or_func_exist
os.environ.setdefault('DJANGO_SETTING_MODULE', 'Management.settings')
django.setup()


def parameter(parameter_id, parameter_type, parameter_text):
    type = Parameter.parameters.get_parameter_type(parameter_type=parameter_type)
    if type == 'key-value':
        try:
            result = json.loads(parameter_text)
            return result
            #将value转换成变量
        except (TypeError, ValueError) as err:
            print('ERROR')#TODO 记日志
    elif type == 'sql':
        try:
            if isinstance(parameter_text, str):
                cursor = connection.cursor()
                cursor.execute(parameter_text)
                result = dict_fetchone(cursor) #只取一个
                cursor.close()
                print(result) #获取对应的字段名
                return get_result_from_sql(parameter_id=parameter_id, result=result)
        except (TypeError) as err:
            print(err)
    elif type == 'replacement':
        if is_var_or_func_exist(parameter_text):
            return parameter_text
        else:
            return parameter_text
            pass#抛出异常
    elif type == 'value':
        return parameter_text
# parameter('sql', 'select * from visa.kfc_order limit 1')
# parameter(1)


def get_result_from_sql(parameter_id, result):
    parameter_sql = ParameterSql.objects.get(parameter=parameter_id)
    type = parameter_sql.type
    column = parameter_sql.column
    if type == 1:
        #取单个值，多个的话取第一个
        return result[0][column]
    elif type == 2:
        return 0

