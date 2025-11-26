#!/usr/bin/env python
"""
Script to run all tests with coverage report
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True, keepdb=False)
    
    # Run all tests
    failures = test_runner.run_tests([
        'accounts.tests',
        'courses.tests',
        'teachers.tests',
        'students.tests',
    ])
    
    sys.exit(bool(failures))
