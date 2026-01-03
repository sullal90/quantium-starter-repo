#!/usr/bin/env python3
"""Simple test runner that executes test_ functions in tests/test_app.py

This is a fallback when pytest is not available in the environment. It runs
each function whose name starts with `test_` and reports pass/fail.
"""
import importlib
import sys
import os

# Ensure project root is on sys.path so `tests` can be imported when this
# script is executed from the `scripts/` directory. When executing
# `python3 scripts/run_tests_no_pytest.py`, sys.path[0] is the scripts
# dir; add parent directory so imports like `tests.test_app` resolve.
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

try:
    tests = importlib.import_module('tests.test_app')
except Exception as e:
    print('ERROR: could not import tests.test_app:', e)
    sys.exit(2)

failures = []
passed = []

for name in dir(tests):
    if name.startswith('test_'):
        obj = getattr(tests, name)
        if callable(obj):
            try:
                obj()
                print(f'{name}: PASS')
                passed.append(name)
            except AssertionError as ae:
                print(f'{name}: FAIL - {ae}')
                failures.append((name, str(ae)))
            except Exception as ex:
                print(f'{name}: ERROR - {ex}')
                failures.append((name, str(ex)))

print('\nSummary:')
print(f'  Passed: {len(passed)}')
print(f'  Failed: {len(failures)}')

if failures:
    sys.exit(1)
else:
    sys.exit(0)
