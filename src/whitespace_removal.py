import shpaml
import runtime

class TextWithoutWhitespace(unicode):
    ''' Part of template that does not need whitespace.
    
    Whitespace removal assumes that:
    
    1. Whitespace can be removed between block tags and their children, and
    
    2. Leading whitespace on the lines of template instructions occupying entire lines
       can be removed.
    
    TextWithoutWhitespace is a marker class that propagates whitespace removal
    status of lines from which whitespace can be removed across string concatenations.
    '''

class WhitespaceRemoval:
    @classmethod
    def install(cls):
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
                    cls = second.__class__
                    copy[0] = cls(first + second)
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
