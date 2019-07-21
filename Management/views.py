from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Management.models import TestCase, TestCases
import os
from django.core import serializers
from django.forms.models import model_to_dict


def testcase_list(request):
    testcases_list = list(TestCase.objects.filter(is_valid=1))
    json_testcase_list = serializers.serialize('json', testcases_list)
    dict_testcase_list = []
    for testcase in testcases_list:
        dict_testcase_list.append(model_to_dict(testcase))
    json_info = {'testcases_list': json_testcase_list}
    dict_info = {'testcases_list': dict_testcase_list}
    path = os.path.join('Management', 'index.html')
    # return HttpResponse(JsonResponse(json_info), content_type="application/json")
    return render(request, path, dict_info)


