import os, os.path, sys, unittest

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.join(root, 'tools'))

def run_tests(source_dir, template):
    print 'Testing %s in %s' % (template, source_dir)
    if os.fork():
        pid, status = os.wait()
        if status > 0 and status < 256:
            exit(status)
        elif status >= 256:
            exit(-1)
    else:
        full_source_path = os.path.join(root, source_dir)
        sys.path.append(full_source_path)
        module = getattr(__import__('tests.%s' % template), template)
        unittest.main(module)

for source_dir in ('src', 'build'):
    for template in ('jinja', 'erb', 'erubis'):
        run_tests(source_dir, template)
