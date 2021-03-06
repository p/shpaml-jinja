import re
import shpaml
import aml
import runtime
import whitespace_removal

class JinjaShortcuts(aml.ShortcutsBase):
    LINE_STATEMENT = aml.fixup(r'^(\s*)%(\s*)(.*)$', re.M, r'\1{%\2\3\2%}')
    LINE_EXPRESSION = aml.fixup(r'^(\s*)=(\s*)(.*)$', re.M, r'\1{{\2\3\2}}')
    SELF_CLOSING_TAG = aml.fixup(r'^(\s*)>(?=\w)', re.M, r'\1> ')
    ENDIF_ELIF = aml.fixup(r'^(\s*){%\s*end(?:el)?if\s*%}\n(\1{%\s*elif\s)', re.M, r'\2')
    ENDIF_ELIF_WITHOUT_WHITESPACE = aml.fixup(r'{%\s*end(?:el)?if\s*%}\n({%\s*elif\s)', None, r'\1')
    ENDIF_ELSE = aml.fixup(r'^(\s*){%\s*end(?:el)?if\s*%}\n(\1{%\s*else\s*%})', re.M, r'\2')
    ENDIF_ELSE_WITHOUT_WHITESPACE = aml.fixup(r'{%\s*end(?:el)?if\s*%}\n({%\s*else\s*%})', None, r'\1')
    ENDELSE = aml.fixup(r'^(\s*){%\s*endel(?:se|if)\s*%}', re.M, r'\1{% endif %}')
    ENDELSE_WITHOUT_WHITESPACE = aml.fixup(r'{%\s*endel(?:se|if)\s*%}', None, r'{% endif %}')
    TRANS_LINE_STATEMENT = aml.fixup(r'^(\s*)~(\s*)(.*)$', re.M, r'\1{% trans %}\3{% endtrans %}')

    PRE_TRANSLATORS = [
        LINE_STATEMENT,
        LINE_EXPRESSION,
        SELF_CLOSING_TAG,
        TRANS_LINE_STATEMENT,
    ]

    POST_TRANSLATORS = [
        ENDIF_ELIF,
        ENDIF_ELSE,
        ENDELSE,
    ]
    
    POST_TRANSLATORS_WITHOUT_WHITESPACE = [
        ENDIF_ELIF_WITHOUT_WHITESPACE,
        ENDIF_ELSE_WITHOUT_WHITESPACE,
        ENDELSE_WITHOUT_WHITESPACE,
    ]
    
    @classmethod
    def install(cls):
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
                    append(prefix + whitespace_removal.TextWithoutWhitespace(tag))
                    recurse(block[1:])
                    append(prefix + whitespace_removal.TextWithoutWhitespace('{% end' + match.group(1) + ' %}'))
                    return
            html_block_tag_without_template_statement(output, block, recurse)
        
        runtime.hook_module_function(shpaml, 'html_block_tag', html_block_tag_with_template_statement)

aml.configure(JinjaShortcuts)
convert_text = aml.convert_text

if __name__ == "__main__":
    import filter
    filter.perform_conversion(convert_text)
