import re
import shpaml
import aml
import runtime
import whitespace_removal

class ErbShortcuts(aml.ShortcutsBase):
    LINE_STATEMENT = aml.fixup(r'^(\s*)%(\s*)(.*)$', re.M, r'\1<%\2\3\2%>')
    LINE_EXPRESSION = aml.fixup(r'^(\s*)=(\s*)(.*)$', re.M, r'\1<%=\2\3\2%>')
    SELF_CLOSING_TAG = aml.fixup(r'^(\s*)>(?=\w)', re.M, r'\1> ')
    END_ELSE = aml.fixup(r'^(\s*)<%\s*end\s*%>\n(\1<%\s*else\s*%>)', re.M, r'\2')
    END_ELSE_WITHOUT_WHITESPACE = aml.fixup(r'<%\s*end\s*%>(<%\s*else\s*%>)', None, r'\1')
    TRANS_LINE_STATEMENT = aml.fixup(r'^(\s*)~(\s*)(.*)$', re.M, r'\1{% trans %}\3{% endtrans %}')

    PRE_TRANSLATORS = [
        LINE_STATEMENT,
        LINE_EXPRESSION,
        SELF_CLOSING_TAG,
        TRANS_LINE_STATEMENT,
    ]

    POST_TRANSLATORS = [
        END_ELSE,
    ]
    
    POST_TRANSLATORS_WITHOUT_WHITESPACE = [
        END_ELSE_WITHOUT_WHITESPACE,
    ]
    
    @classmethod
    def install(cls):
        ''' Installs various shortcuts intended to be used with Embedded Ruby (ERb) templates.
        
        Specifically, allows for the following markup in templates:
        
        1. Automatic generation of appropriate closing tags for template instructions:
        
        % if
            ...
        % else
            ...
        
        2. '% tag' shortcut as a replacement for '<% tag %>', and corresponding
           shpaml-style self-closing tag:
        
        % block bar
            ...
        
        % >block
        
        3. '>tag' is equivalent to '> tag'.
        
        4. '= expression' is equivalent to '<%= expression %>'
        
        5. '~ text' is equivalent to '{% trans %}text{% endtrans %}'
        '''
        
        @shpaml.syntax(r'{% > *((\w+).*)')
        def SELF_CLOSING_TEMPLATE_STATEMENT(m):
            tag = m.group(1).strip()
            return '<%% %s<%% end %%>' % (m.group(1))
        
        shpaml.LINE_METHODS.insert(0, SELF_CLOSING_TEMPLATE_STATEMENT)
        
        TEMPLATE_STATEMENT = re.compile(r'<% (\w+)')
        
        def html_block_tag_with_template_statement(html_block_tag_without_template_statement, output, block, recurse):
            append = output.append
            prefix, tag = block[0]
            if shpaml.RAW_HTML.regex.match(tag):
                match = TEMPLATE_STATEMENT.match(tag)
                if match:
                    append(prefix + whitespace_removal.TextWithoutWhitespace(tag))
                    recurse(block[1:])
                    append(prefix + whitespace_removal.TextWithoutWhitespace('<% end %>'))
                    return
            html_block_tag_without_template_statement(output, block, recurse)
        
        runtime.hook_module_function(shpaml, 'html_block_tag', html_block_tag_with_template_statement)

aml.configure(ErbShortcuts)
convert_text = aml.convert_text

if __name__ == "__main__":
    import filter
    filter.perform_conversion(convert_text)
