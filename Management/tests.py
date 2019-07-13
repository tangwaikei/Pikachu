import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pikachu.settings')
django.setup()
from Management.Support.runner import run_testcases


run_testcases(2)
