#!/usr/bin/env python

import sys, os.path, re
import file_utils

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
    use_re = re.compile(r'%s\.(\w)' % modules)
    text = use_re.sub(r'\2', text)
    return text

def fix_convert_text_callers(text):
    return re.sub(r'\b(\w+)\.convert_text\(', r'convert_text_\1(', text)

def rename_convert_text(text, module):
    return re.sub(r'\bconvert_text\b', 'convert_text_' + module, text)

args = sys.argv[1:]
sources = args[:-1]
target = args[-1]

merged_module_names = {}
for path in sources[1:]:
    merged_module_names[path] = re.sub(r'\.py$', '', os.path.basename(path))

text = fix_convert_text_callers(file_utils.read_file(sources[0]))
for source in sources[1:]:
    text += rename_convert_text(strip_main(file_utils.read_file(source)), merged_module_names[source])
text = move_main(strip_modules(text, merged_module_names.values()))

f = open(target, 'w')
try:
    f.write(text)
finally:
    f.close()
