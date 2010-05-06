import re

''' Aml is a pre/post-processor for shpaml. It extends shpaml syntax
with shortcuts useful when shpaml output is a jinja template.

Aml module can be imported into a Python program and used as follows:

import aml
jinja_template_text = aml.convert_text(aml_template_text)

Alternatively, aml.py can be invoked from the command line to perform
the conversion, as follows:

python aml.py [-o output] [input]

If input is not specified or is - (dash), standard input is read.
If output is not specified or is -, processed text is written to
standard output.

Aml depends on other modules as follows:

shpaml does most of the work. It is patched at runtime so arbitrary
versions of it are unlikely to work.

runtime provides functions for hooking into modules, used to inject
code into shpaml at runtime.

filter provides command line argument handling. It is only used when
aml.py is invoked from command line.

'''

# Aml works with unmodified shpaml but certain versions may be required
# depending on shortcuts used since aml patches shpaml's code at runtime.
# A version of shpaml that is known to work is bundled with aml.
import shpaml
import runtime

class IndentError(ValueError):
    ''' Raised when text given to aml uses tabs for indentation.
    
    Mixing tabs and spaces in aml templates can have disastrous consequences,
    therefore indenting with tabs is prohibited.
    '''

def convert_text(text):
    ''' Converts text to html. Text must be in aml template format (at).
    
    Aml templates are mostly comprised of shpaml syntax with shortcuts
    added for jinja. Please refer to install_jinja_shortcuts for syntax
    details.
    
    Whitespace removal is enabled; please refer to install_whitespace_removal
    for details on what whitespace is removed. Whitespace removal is not
    necessary to generate valid html from aml templates.
    
    Whitespace removal is an experimental feature.
    
    Indentation in aml is significant, and only spaces are allowed for
    indentation. If tabs are found in text at the beginning of any lines,
    IndentError will be raised.
    '''
    
    install_jinja_shortcuts()
    install_whitespace_removal()
    text = convert_text_pre(text)
    text = shpaml.convert_text(text)
    text = convert_text_post(text)
    return text

# Only implementation is beyond this point.

TAB_INDENT = re.compile(r'^ *\t', re.M)

def fixup(regex, flags, replacement):
    if flags is not None:
        options = [flags]
    else:
        options = []
    regex = re.compile(regex, *options)
    return (regex, replacement)

LINE_STATEMENT = fixup(r'^(\s*)%(\s*)(.*)$', re.M, r'\1{%\2\3\2%}')
LINE_EXPRESSION = fixup(r'^(\s*)=(\s*)(.*)$', re.M, r'\1{{\2\3\2}}')
SELF_CLOSING_TAG = fixup(r'^(\s*)>(?=\w)', re.M, r'\1> ')
ENDIF_ELSE = fixup(r'^(\s*){%\s*endif\s*%}\n(\1{%\s*else\s*%})', re.M, r'\2')
ENDIF_ELSE_WITHOUT_WHITESPACE = fixup(r'{%\s*endif\s*%}({%\s*else\s*%})', None, r'\1')
ENDELSE = fixup(r'^(\s*){%\s*endelse\s*%}', re.M, r'\1{% endif %}')
ENDELSE_WITHOUT_WHITESPACE = fixup(r'{%\s*endelse\s*%}', None, r'{% endif %}')
TRANS_LINE_STATEMENT = fixup(r'^(\s*)~(\s*)(.*)$', re.M, r'\1{% trans %}\3{% endtrans %}')

PRE_TRANSLATORS = [
    LINE_STATEMENT,
    LINE_EXPRESSION,
    SELF_CLOSING_TAG,
    TRANS_LINE_STATEMENT,
]

POST_TRANSLATORS = [
    ENDIF_ELSE,
    ENDELSE,
]

def convert_text_pre(text):
    ''' Performs pre-processing pass on text before handing it off to shpaml.
    
    First, indentation is checked and if tabs are used for indentation
    IndentError is raised.
    
    Then, jinja shortcuts in text are replaced with expanded equivalents.
    '''
    
    if TAB_INDENT.search(text):
        raise IndentError('Text uses tabs for indentation')
    
    for translator in PRE_TRANSLATORS:
        text = translator[0].sub(translator[1], text)
    
    return text

def convert_text_post(text):
    ''' Performs post-processing pass on text after it is processed by shpaml.
    
    Post-processing fixes up things like if/endif/else/endelse into if/else/endif.'
    '''
    
    for translator in POST_TRANSLATORS:
        text = translator[0].sub(translator[1], text)
    
    return text

class TextWithoutWhitespace(unicode):
    ''' Part of template that does not need whitespace.
    
    Whitespace removal assumes that:
    
    1. Whitespace can be removed between block tags and their children, and
    
    2. Leading whitespace on the lines of template instructions occupying entire lines
       can be removed.
    
    TextWithoutWhitespace is a marker class that propagates whitespace removal
    status of lines from which whitespace can be removed across string concatenations.
    '''

_hooks_installed = dict()

def install_jinja_shortcuts():
    ''' Installs various shortcuts intended to be used with Jinja (version 2) templates.
    
    Specifically, allows for the following markup in templates:
    
    1. Automatic generation of appropriate closing tags for template instructions:
    
    % if
        ...
    % else
        ...
    
    2. '% tag' shortcut as a replacement for '{% tag %}', and corresponding
       shpaml-style self-closing tag:
    
    % block bar
        ...
    
    % >block
    
    3. '>tag' is equivalent to '> tag'.
    
    4. '= expression' is equivalent to '{{ expression }}'
    
    5. '~ text' is equivalent to '{% trans %}text{% endtrans %}'
    '''
    
    global _hooks_installed
    if not _hooks_installed.has_key('jinja_shortcuts'):
        @shpaml.syntax(r'{% > *((\w+).*)')
        def SELF_CLOSING_TEMPLATE_STATEMENT(m):
            tag = m.group(1).strip()
            return '{%% %s{%% end%s %%}' % (m.group(1), m.group(2))
        
        shpaml.LINE_METHODS.insert(0, SELF_CLOSING_TEMPLATE_STATEMENT)
        
        TEMPLATE_STATEMENT = re.compile(r'{% (\w+)')
        
        def html_block_tag_with_template_statement(html_block_tag_without_template_statement, output, block, recurse):
            append = output.append
            prefix, tag = block[0]
            if shpaml.RAW_HTML.regex.match(tag):
                match = TEMPLATE_STATEMENT.match(tag)
                if match:
                    append(prefix + TextWithoutWhitespace(tag))
                    recurse(block[1:])
                    append(prefix + TextWithoutWhitespace('{% end' + match.group(1) + ' %}'))
                    return
            html_block_tag_without_template_statement(output, block, recurse)
        
        runtime.hook_module_function(shpaml, 'html_block_tag', html_block_tag_with_template_statement)
        
        _hooks_installed['jinja_shortcuts'] = True

def install_whitespace_removal():
    ''' Installs smart whitespace removal logic.
    
    Shpaml provides for two syntaxes for putting text inside tags:
    
    a href=foo
        bar
    
    generates:
    
    <a href="foo">
        bar
    </a>
    
    and
    
    a href=foo |bar
    
    generates:
    
    <a href="foo">bar</a>
    
    "bar" in this example can become quite complex if a template engine
    is used and it is actually an expression. Furthermore jinja shortcuts
    above work on line level only.
    
    Whitespace removal allows this markup:
    
    a href=foo
        ~ bar
    
    to be converted to:
    
    <a href="foo">{% trans %}bar{% endtrans %}</a>
    
    instead of:
    
    <a href="foo">
        {% trans %}bar{% endtrans %}
    </a>
    
    The assumption is that whitespace can always be removed between a block
    tag and its children.
    
    Nested tags behave as expected:
    
    ul
        li
            a href=foo
                bar
    
    generates:
    
    <ul><li><a href="foo">bar</a></li></ul>
    
    Significant whitespace may be emitted via tools provided by template
    engine, for example:
    
    a href=foo
        = ' bar'
    
    If whitespace removal is installed, leading whitespace on lines containing
    only template instructions (% shortcut) or that start with block tags will
    also be removed.
    '''
    
    global _hooks_installed
    if not _hooks_installed.has_key('whitespace_removal'):
        class StartBlockTag(TextWithoutWhitespace):
            pass
        
        class EndBlockTag(TextWithoutWhitespace):
            pass
        
        class Line(TextWithoutWhitespace):
            pass
        
        def convert_line_with_whitespace_removal(convert_line_without_whitespace_removal, line):
            line = convert_line_without_whitespace_removal(line)
            return Line(line)
        
        def apply_jquery_sugar_with_whitespace_removal(apply_jquery_sugar_without_whitespace_removal, markup):
            start_tag, end_tag = apply_jquery_sugar_without_whitespace_removal(markup)
            return (StartBlockTag(start_tag), EndBlockTag(end_tag))
        
        class Indentation(unicode):
            def __add__(self, other):
                if isinstance(other, TextWithoutWhitespace):
                    return other
                else:
                    return unicode.__add__(self, other)
        
        def indent_lines_with_whitespace_removal(
            indent_lines_without_whitespace_removal,
            lines,
            output,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block,
        ):
            # output is modified
            indent_lines_without_whitespace_removal(
                lines,
                output,
                branch_method,
                leaf_method,
                pass_syntax,
                flush_left_syntax,
                flush_left_empty_line,
                indentation_method,
                get_block,
            )
            
            # need to modify output in place
            copy = list(output)
            while len(output) > 0:
                output.pop()
            while len(copy) > 1:
                first, second = copy[:2]
                if len(copy) >= 3:
                    third = copy[2]
                else:
                    third = None
                if isinstance(second, EndBlockTag):
                    if isinstance(third, EndBlockTag):
                        copy[1] = EndBlockTag(second + third)
                        copy.pop(2)
                    else:
                        output.append(first + second)
                        copy.pop(0)
                        copy.pop(0)
                elif isinstance(first, StartBlockTag):
                    copy[0] = StartBlockTag(first + second)
                    copy.pop(1)
                else:
                    output.append(first)
                    copy.pop(0)
            if len(copy) > 0:
                output.append(copy[0])
        
        def find_indentation_with_whitespace_removal(find_indentation_without_whitespace_removal, line):
            prefix, line = find_indentation_without_whitespace_removal(line)
            return (Indentation(prefix), line)
        
        runtime.hook_module_function(shpaml, 'convert_line', convert_line_with_whitespace_removal)
        runtime.hook_module_function(shpaml, 'apply_jquery_sugar', apply_jquery_sugar_with_whitespace_removal)
        runtime.hook_module_function(shpaml, 'indent_lines', indent_lines_with_whitespace_removal)
        runtime.hook_module_function(shpaml, 'find_indentation', find_indentation_with_whitespace_removal)
        
        # We replace post translators because original implementations cannot
        # match anything when whitespace removal is enabled.
        POST_TRANSLATORS.remove(ENDIF_ELSE)
        POST_TRANSLATORS.append(ENDIF_ELSE_WITHOUT_WHITESPACE)
        POST_TRANSLATORS.remove(ENDELSE)
        POST_TRANSLATORS.append(ENDELSE_WITHOUT_WHITESPACE)
        
        _hooks_installed['whitespace_removal'] = True

# This small hack is needed for single-file distribution, since shpaml
# also defines a convert_text function.
convert_text_aml = convert_text

if __name__ == "__main__":
    import filter
    filter.perform_conversion(convert_text_aml)
