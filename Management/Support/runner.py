import os
import io
import re
import shutil
from threading import Thread
from django.core.exceptions import ObjectDoesNotExist
from Management.models import TestCase, Parameter, TestCases, TestSuites, Action
from Management.Support.parameter import parameter
from Management.Support.util import testcase_to_yml, isset_var
from httprunner.api import HttpRunner


def single_son_testcase(testcase, son_testcase, path, is_bulk):
    try:
        # 递归
        match = re.match('([a-zA-Z]*)\s.*', testcase.name)
        if match:
            son_path = match.group(1)
        else:
            son_path = '{}_son'.format(testcase.name).rstrip('.')
        is_son_bulk = len(list(son_testcase)) > 0
        son_yaml_path = os.path.join(path, son_path + '.yml')
        for son_testcase in list(son_testcase):
            single_testcase(son_testcase, son_yaml_path, is_son_bulk)
        # config
        name = testcase.name
        yaml = {}
        yaml['test'] = {}
        yaml['test']['name'] = name
        if not is_bulk:
            testcase_yml_path = os.path.join(path, '{}.yml'.format(testcase.name))
        else:
            testcase_yml_path = path + '.yml'
        # 组装成yml
        if son_yaml_path:
            yaml['test']['testcase'] = son_yaml_path
        else:
            yaml['test']['testcase'] = testcase_yml_path
        if not os.path.exists(testcase_yml_path):
            with open(testcase_yml_path, 'a') as f:
                pass
        # 写入文件
        testcase_to_yml(testcase_yml_path, yaml)
    except ObjectDoesNotExist:
        return ''


def single_testcase(testcase, path, is_bulk):
    try:
        testcase_id = testcase.id
        son_testcase = TestCase.objects.filter(parent=testcase_id)
        has_son_testcase = len(list(son_testcase)) > 0
        if has_son_testcase:
           single_son_testcase(testcase, son_testcase, path, is_bulk)
        else:
            testcase_parameter = Parameter.parameters.filter(testcase=testcase_id, testcaseparameter__is_valid=1)
            testcase_action = Action.objects.filter(testcase=testcase_id, testcaseaction__is_valid=1)
            # config
            name = testcase.name
            url = testcase.url
            url_type = testcase.url_type
            yaml = {}
            yaml['test'] = {}
            yaml['test']['name'] = name
            yaml['test']['variables'] = {}
            for i in list(testcase_parameter):
                yaml['test']['variables'][i.name] = parameter(parameter_id=i.id, parameter_type=i.parameter_type,
                                                              parameter_text=i.parameter)
            if not len(yaml['test']['variables']):
                del yaml['test']['variables']
            for i in list(testcase_action):
                if i.action_type == 1:
                    column_name = 'setup_hooks'
                elif i.action_type == 2:
                    column_name = 'teardown_hooks'
                if isset_var(column_name):
                    yaml['test'][column_name][i.name] = i.action
            if len(url):
                if url_type == 0:
                    pass
                elif url_type == 1:
                    url_name = 'base_url'
                    yaml['test'][url_name] = url
                elif url_type == 2:
                    url_name = 'api'
                    yaml['test'][url_name] = url
            if testcase.request:
                yaml['test']['request'] = testcase.request
            yaml['test']['validate'] = ''  # TODO
            path_match = re.match('.*\.yml$', path)
            if not path_match:
                # 组装debugtalk.py
                if not os.path.exists(path.strip()):
                    path = path.strip()
                    os.makedirs(path)
                debugtalk_py_path = os.path.join(path.strip(), 'debugtalk.py')
                if not os.path.exists(debugtalk_py_path):
                    with io.open(debugtalk_py_path, 'w') as f:
                        f.write('# encoding: utf-8')
                src = "base_debugtalk.py"
                dst = debugtalk_py_path
                Thread(target=shutil.copy, args=[src, dst]).start()
                testcase_yml_path = '{}.yml'.format(path)
            else:
                testcase_yml_path = path
            if not os.path.exists(testcase_yml_path):
                with open(testcase_yml_path, 'a') as f:
                    pass
            #写入文件
            testcase_to_yml(testcase_yml_path, yaml)
    except ObjectDoesNotExist:
        return ''


def run_testcases(testcases_id):
    testcases = TestCases.objects.get(id=testcases_id)
    testcases_name = testcases.name
    group = testcases.group
    group_name = group.name
    testcases = TestCase.objects.filter(testcases=testcases_id, is_valid=1, parent=0)
    testcases_list = list(testcases)
    is_bulk = len(testcases_list)
    for testcase in testcases_list:
        path = os.path.join('TestSuiteYaml', group_name, testcases_name)
        single_testcase(testcase, path, is_bulk)
    testcase_yml_path = os.path.join('TestSuiteYaml', group_name, testcases_name)
    testcase_yml_path = '{}.yml'.format(testcase_yml_path)
    runner = HttpRunner(failfast=True)
    runner.run(testcase_yml_path)










