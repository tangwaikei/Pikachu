from django.db import models


class TestCaseManager(models.Manager):
    def get_object(self, test_case_id):  # 根据parameter得到一条数据
        return self.get(id=test_case_id)


class ParametersManager(models.Manager):
    def get_object(self, parameter_id):  # 根据parameter得到一条数据
        return self.get(id=parameter_id)

    @staticmethod
    def get_parameter_type(self, parameter_type):
        if parameter_type == 1:
            return 'key-value'
        if parameter_type == 2:
            return 'sql'
        if parameter_type == 3:
            return 'testcase_result'


class ParameterSqlManager(models.Manager):
    def get_object(self, parameter_id):  # 根据parameter得到一条数据
        return self.get(parameter=parameter_id)


class ActionManager(models.Manager):
    def get_object(self, parameter_id):  # 根据parameter得到一条数据
        return self.get(parameter=parameter_id)


class TestCaseParameterManager(models.Manager):
    def get_object(self, testcase_id):  # 根据parameter得到一条数据
        return self.get(testcase=testcase_id)


class TestSuiteManager(models.Manager):
    def get_object(self, testsuite_id):  # 根据parameter得到一条数据
        return self.get(id=testsuite_id)