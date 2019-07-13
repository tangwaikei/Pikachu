import os
import io
import json
import shutil
from threading import Thread
from django.core.exceptions import ObjectDoesNotExist
from httprunner.api import HttpRunner
from httprunner.parser import is_var_or_func_exist
from Management.models import TestCase, TestCaseParameter, Parameter, TestCases, TestSuites, Action
from Management.Support.parameter import parameter
from Management.Support.util import testcase_to_yml, isset_var
from Management import separator


def single_testcase(testcase_id, path, is_bulk):
    try:
        testcase = TestCase.objects.get_object(test_case_id=testcase_id)
        # testcase_parameter = TestCaseParameter.objects.filter(testcase=testcase_id, is_valid=1).all()
        testcase_parameter = Parameter.parameters.filter(testcase=1, testcaseparameter__is_valid=1)
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
            yaml['test']['variables'][i.name] = parameter(parameter_id=i.id, parameter_type=i.parameter_type, parameter_text=i.parameter)
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
        yaml['test']['validate'] = ''#TODO
        print(yaml)
        #组装debugtalk.py
        path = path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
        debugtalk_py_path = os.path.join(path.strip(), 'debugtalk.py')
        if not os.path.exists(debugtalk_py_path):
            with io.open(debugtalk_py_path, 'w') as f:
                f.write('# encoding: utf-8')
        src = "base_debugtalk.py"
        dst = debugtalk_py_path
        Thread(target=shutil.copy, args=[src, dst]).start()
        #组装成yml
        if not is_bulk:
            testcase_yml_path = os.path.join(path, '{}.yml'.format(testcase.name))
        else:
            testcase_yml_path = path + '.yml'
        if not os.path.exists(testcase_yml_path):
            os.mknod(testcase_yml_path)
        #写入文件
        testcase_to_yml(testcase_yml_path, yaml)
    except ObjectDoesNotExist:
        return ''
    pass
    # runner = HttpRunner(failfast=True)
    # runner.run(testcase_yml_path)


def batch_testcases(testsuite_id):
    testcases = TestCases.objects.get(id=testsuite_id)
    group = testcases.group
    print(group)
    group_name = group.name
    testcase_list = TestCase.objects.filter(testcases=1).order_by('seq')
    testsuite_path = os.path.join('TestSuiteYaml', group_name, testcases.name)
    if not testsuite_path:
        os.mkdir(testsuite_path)
    testcase_list = list(testcase_list)
    is_bulk = len(testcase_list) > 0
    for testcase in list(testcase_list):
        path = os.path.join(testsuite_path, testcase.name)
        single_testcase(testcase.id, path, is_bulk)


def run_testcases(testcases_id):
    testcases = TestCases.objects.get(id=testcases_id)
    testcases_name = testcases.name
    group = testcases.group
    group_name = group.name
    print(group)
    testcases = TestCase.objects.filter(testcases=testcases_id, is_valid=1)
    testcases_list = list(testcases)
    is_bulk = len(testcases_list)
    for testcase in testcases_list:
        path = os.path.join('TestSuiteYaml', group_name, testcases_name)
        single_testcase(testcase.id, path, is_bulk)
        # parameter = Parameter.parameters.filter(testcase=testcase.id, testcaseparameter__is_valid=1)
        # parameter_list = list(parameter)
        # for parameter_object in parameter_list:










