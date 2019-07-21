from django.shortcuts import render
from Management.models import TestCase, TestCases
import os
from django.shortcuts import render_to_response


def testcase_list(request):
    testcases_list = TestCase.objects.filter(is_valid=1)
    info = {'a': 2}
    path = os.path.join('Management', 'index.html')
    return render_to_response(path, info)


