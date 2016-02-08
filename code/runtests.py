#!/usr/bin/env python

from subprocess import call
from pathlib import Path
from os import remove
from sys import argv

code_dir, tests_dir = 'woodhouse', 'tests'
root = Path(__file__).parent


def iter_files(glob):
    for dirname in [code_dir, tests_dir]:
        yield from root.joinpath(dirname).glob('**/%s' % glob)


print('Checking for pdb calls')
for path in iter_files('*.py'):
    with path.open() as fp:
        for lnum, line in enumerate(fp, 1):
            if 'pdb.set_trace()' in line:
                raise SystemExit('error: %s:%d: pdb call' % (path, lnum))


print('Cleaning .pyc files...')
for path in iter_files('*.pyc'):
    if 'venv' in path.parts:
        continue
    remove(str(path))

print('running flake8...')
code = call(['flake8', code_dir, tests_dir])
if code != 0:
    raise SystemExit(code)

print('running tests...')
cmd = ['python', '-m', 'unittest', 'discover']
if len(argv) == 1:
    cmd += ['-v', 'tests']
else:
    argv[1:]

code = call(cmd)
raise SystemExit(code)
