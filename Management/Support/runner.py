import os
from django.core.exceptions import ObjectDoesNotExist
from Management.models import TestCase, TestCaseParameter, Parameter, TestSuites
from httprunner.api import HttpRunner
from Management.Support.parameter import parameter
from Management.Support.util import testcase_to_yml


def single_testcase(testcase_id, path):
    try:
        testcase = TestCase.objects.get_object(test_case_id=testcase_id)
        testcase_parameter = TestCaseParameter.objects.filter(testcase=testcase_id, is_valid=1).all()
        testcase_parameter = Parameter.parameters.filter(testcase=1, testcaseparameter__is_valid=1)

        # config
        name = testcase.name
        url = testcase.url
        yaml = {}
        yaml['test']['name'] = name
        yaml['test']['variables'] = []
        for i in list(testcase_parameter):
            yaml['test']['variables'][i.name] = parameter(parameter_id=i.id, parameter_type=i.parameter_type, parameter_text=i.parameter)
        if len(url):
            yaml['test']['api'] = url
        yaml['test']['request'] = testcase.load(testcase.request)
        yaml['test']['validate'] = ''#TODO
        #组装成yml
        testcase_yml_path = os.path.join(path, testcase.name + '.yml')
        if not testcase_yml_path:
            os.mkdir(testcase_yml_path)
        #写入文件
        testcase_to_yml(testcase_yml_path, yaml)
    except ObjectDoesNotExist:
        return ''
    pass
    runner = HttpRunner(failfast=True)
    runner.run(testcase_yml_path)


def suite(testsuite_id):
    testsuite = TestSuites.objects.get(id=testsuite_id)
    group = testsuite.groups
    group_name = group.name
    testcases = TestCase.objects.filter(testsuite=1).order_by('seq')
    testsuite_path = os.path.join('TestSuiteYaml', group_name, testsuite.name)
    for testcase in list(testcases):
        path = os.path.join(testsuite_path, testcase.name)
        single_testcase(testcase.id, path)






