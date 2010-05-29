#!/usr/bin/env python

import sys, os.path, re, optparse
import file_utils

parser = optparse.OptionParser()
parser.add_option('-o', '--output', help='Store output in FILE', metavar='FILE')
parser.add_option('-m', '--main', help='Indicate module MODULE is main', metavar='MODULE')

options, args = parser.parse_args()

main_re_text = r'if __name__ == ([\'"])__main__\1:(\n(\s+).*)+\n'
main_re = re.compile(main_re_text)

def strip_main(text):
    return main_re.sub('', text)

def move_main(text):
    text_re = re.compile(r'^(.*)(\nif __name__ == ([\'"])__main__\3:(\n(\s+)[^\n]*)+\n)(.*)$', re.S)
    return text_re.sub(r'\1\n\6\2', text)

def strip_modules(text, modules):
    kill_modules, keep_modules = [], []
    for module in modules:
        if re.search(r'hook_module_function\(%s' % module, text):
            keep_modules.append(module)
        else:
            kill_modules.append(module)
    
    modules = '('+'|'.join(keep_modules)+')'
    import_re = re.compile(r'^(\s*)import %s\n' % '(shpaml)', re.M)
    # usage of hook_module_function necessitates this ugly hack
    text = import_re.sub(r'\1import sys\n\1\2 = sys.modules[__name__]\n', text)
    
    modules = '('+'|'.join(kill_modules)+')'
    import_re = re.compile(r'^\s*import %s\n' % modules, re.M)
    text = import_re.sub('', text)
    use_re = re.compile(r'\b%s\.(\w)' % modules)
    text = use_re.sub(r'\2', text)
    return text

def fix_convert_text_callers(text):
    return re.compile(r'\b(\w+)\.convert_text(\(|$)', re.M).sub(r'convert_text_\1\2', text)

def rename_convert_text(text, module):
    return re.sub(r'\bconvert_text\b', 'convert_text_' + module, text)

sources = args
if options.output:
    target = options.output
else:
    target = None

module_names = {}
for path in sources:
    module_names[path] = re.sub(r'\.py$', '', os.path.basename(path))

if options.main:
    main = options.main
else:
    main = module_names[sources[0]]

text = ''
for source in sources:
    module = module_names[source]
    content = fix_convert_text_callers(file_utils.read_file(source))
    if module == main:
        text += content
    else:
        text += rename_convert_text(strip_main(content), module)
text = move_main(strip_modules(text, module_names.values()))

if target is None:
    print text
else:
    f = open(target, 'w')
    try:
        f.write(text)
    finally:
        f.close()
