from django.urls import path
from Management import views


urlpatterns = [
    path('list', views.testcase_list),
]