from django.db import models
from django.utils import timezone

from Management.managers import ParametersManager, ParameterSqlManager, ActionManager, TestCaseManager, TestCaseParameterManager, TestSuiteManager


# Create your models here.
class BaseTable(models.Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', default=timezone.now)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'


class Group(BaseTable):
    class Meta:
        verbose_name = '组'
        db_table = 'Group'

    name = models.CharField('名称', max_length=20, null=False)
    desc = models.CharField('描述', max_length=30, null=False)
    is_valid = models.BooleanField(null=False, default=1)


class Service(BaseTable):
    class Meta:
        verbose_name = '前后置动作'
        db_table = 'Service'

    name = models.CharField('名称', max_length=20, null=False)
    desc = models.CharField('描述', max_length=30, null=False)


class User(BaseTable):
    class Meta:
        verbose_name = '用户'
        db_table = 'User'

    name = models.CharField('名称', max_length=20, null=False)
    email = models.EmailField('邮件', null=False)
    is_valid = models.BooleanField(null=False, default=1)


class Action(BaseTable):
    class Meta:
        verbose_name = '前后置动作'
        db_table = 'Action'

    name = models.CharField('名称', max_length=20, null=False)
    desc = models.CharField('描述', max_length=30, null=False)
    action = models.TextField('前后置动作', null=False)
    action_type = models.SmallIntegerField('动作类型1前置2后置', null=False)
    type = models.IntegerField('动作的种类')
    is_valid = models.BooleanField(null=False, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = ActionManager()


class Config(BaseTable):
    class Meta:
        verbose_name = '配置'
        db_table = 'config'

    name = models.CharField('名称', max_length=20, null=False)
    base_url = models.CharField('base_url', max_length=100)


class Parameter(BaseTable):
    class Meta:
        verbose_name = '参数'
        db_table = 'Parameter'

    name = models.CharField('名称', max_length=20, null=False)
    desc = models.CharField('描述', max_length=30, null=False)
    parameter_type = models.IntegerField('1key-value2sql3测试用例执行结果')
    parameter = models.TextField('参数')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    parameters = ParametersManager()


class Validate(BaseTable):
    class Meta:
        verbose_name = '校验结果'
        db_table = 'Validate'

    desc = models.CharField('描述', max_length=30, null=False)
    validator = models.TextField('检验')
    type = models.IntegerField('校验种类')
    is_valid = models.BooleanField('是否有效', null=False, default=1)


class TestSuites(BaseTable):
    class Meta:
        verbose_name = '测试用例集'
        db_table = 'TestSuites'

    name = models.CharField('名称', max_length=20, null=False, default='')
    is_valid = models.BooleanField('是否有效', null=False, default=1)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)
    objects = TestSuiteManager()


class TestCase(BaseTable):
    class Meta:
        verbose_name = '测试用例'
        db_table = 'TestCase'

    name = models.CharField('名称', max_length=20, null=False)
    desc = models.CharField('描述', max_length=30, null=False)
    is_valid = models.BooleanField('是否有效', null=False, default=1)
    status = models.BooleanField('0待测试1测试中2已测试', null=False, default=1)
    test_status = models.BooleanField('1测试通过2测试失败', null=False, default=1)
    url = models.CharField('请求链接', max_length=200, null=False, default=1)
    request = models.CharField('请求信息', max_length=300, null=False)
    method = models.CharField('脚本方法', max_length=100, null=False)
    seq = models.IntegerField('顺序', null=False, default=1)
    parameters = models.ManyToManyField(
        Parameter,
        through='TestCaseParameter',
        through_fields=('testcase', 'parameter'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testsuite = models.ForeignKey(TestSuites, on_delete=models.CASCADE, null=True)
    objects = TestCaseManager()


class ParameterSql(BaseTable):
    class Meta:
        verbose_name = '测试用例sql执行表'
        db_table = 'ParameterSql'
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    column = models.CharField('字段名', max_length=20, null=False)
    type = models.IntegerField('校验种类')
    objects = ParameterSqlManager()


class TestCaseValidate(BaseTable):
    class Meta:
        verbose_name = '测试用例校验结果对应表'
        db_table = 'TestCaseValidate'

    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    validate = models.ForeignKey(Validate, on_delete=models.CASCADE)
    seq = models.IntegerField('顺序')
    is_valid = models.BooleanField('是否有效', null=False, default=1)


class TestCaseParameter(BaseTable):
    class Meta:
        verbose_name = '测试用例参数对应表'
        db_table = 'TestCaseParameter'

    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    seq = models.IntegerField('顺序')
    is_valid = models.BooleanField('是否有效', null=False, default=1)
    objects = TestCaseParameterManager()


class TestCaseAction(BaseTable):
    class Meta:
        verbose_name = '测试用例前后置对应表'
        db_table = 'TestCaseAction'

    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    seq = models.IntegerField('顺序')
    is_valid = models.BooleanField('是否有效', null=False, default=1)
    type = models.IntegerField('前置1后置2')
    is_log = models.BooleanField('是否记录', null=False, default=1)


class TestCaseConfig(BaseTable):
    class Meta:
        verbose_name = '测试用例配置'
        db_table = 'TestCaseConfig'

    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    config = models.ForeignKey(Config, on_delete=models.CASCADE)