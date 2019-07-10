import os, io
from django.core.exceptions import ObjectDoesNotExist
from Management.models import TestCase, TestCaseParameter, Parameter, TestCases, TestSuites, Action
from httprunner.api import HttpRunner
from Management.Support.parameter import parameter
from Management.Support.util import testcase_to_yml, isset_var
import shutil
from threading import Thread


def single_testcase(testcase_id, path, is_bulk):
    try:
        testcase = TestCase.objects.get_object(test_case_id=testcase_id)
        # testcase_parameter = TestCaseParameter.objects.filter(testcase=testcase_id, is_valid=1).all()
        testcase_parameter = Parameter.parameters.filter(testcase=1, testcaseparameter__is_valid=1)
        testcase_action = Action.objects.filter(testcase=testcase_id, testcaseaction__is_valid=1)
        # config
        name = testcase.name
        url = testcase.url
        yaml = {}
        yaml['test']['name'] = name
        yaml['test']['variables'] = []
        for i in list(testcase_parameter):
            yaml['test']['variables'][i.name] = parameter(parameter_id=i.id, parameter_type=i.parameter_type, parameter_text=i.parameter)
        for i in list(testcase_action):
            if i.action_type == 1:
                column_name = 'setup_hooks'
            elif i.action_type == 2:
                column_name = 'teardown_hooks'
            if isset_var(column_name):
                yaml['test'][column_name][i.name] = i.action
        if len(url):
            yaml['test']['api'] = url
        yaml['test']['request'] = testcase.load(testcase.request)
        yaml['test']['validate'] = ''#TODO
        #组装debugtalk.py
        debugtalk_py_path = os.path.join(path, 'debugtalk.py')
        if not os.path.exists(debugtalk_py_path):
            with io.open(debugtalk_py_path, 'w') as f:
                f.write('# encoding: utf-8')
            src = "base_debugtalk.py"
            dst = debugtalk_py_path
            Thread(target=shutil.copy, args=[src, dst]).start()
        #组装成yml
        if not is_bulk:
            testcase_yml_path = os.path.join(path, testcase.name + '.yml')
        else:
            testcase_yml_path = path + '.yml'
        if not testcase_yml_path:
            os.mkdir(testcase_yml_path)
        #写入文件
        testcase_to_yml(testcase_yml_path, yaml)
    except ObjectDoesNotExist:
        return ''
    pass
    runner = HttpRunner(failfast=True)
    runner.run(testcase_yml_path)


def batch_testcases(testsuite_id):
    testcases = TestCases.objects.get(id=testsuite_id)
    group = testcases.groups
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


def run_testsuite(testsuite_id):
    testsuite = TestSuites.objects.get(id=testsuite_id)

    pass






