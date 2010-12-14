import re
import shpaml
import aml
import runtime
import whitespace_removal

class ErbShortcuts(aml.ShortcutsBase):
    LINE_STATEMENT = aml.fixup(r'^(\s*)%(?!%)(\s*)(.*)$', re.M, r'\1<%\2\3\2%>')
    LINE_EXPRESSION = aml.fixup(r'^(\s*)=(\s*)(.*)$', re.M, r'\1<%=\2\3\2%>')
    PREPROCESSED_LINE_STATEMENT = aml.fixup(r'^(\s*)!(?!!)(\s*)(.*)$', re.M, r'\1<%!\2\3\2%>')
    PREPROCESSED_LINE_EXPRESSION = aml.fixup(r'^(\s*)!(?:[!=])(\s*)(.*)$', re.M, r'\1<%!=\2\3\2%>')
    SELF_CLOSING_TAG = aml.fixup(r'^(\s*)>(?=\w)', re.M, r'\1> ')
    END_ELSE = aml.fixup(r'^(\s*)<%(!?)\s*end\s*%>\n(\1<%\2\s*else\s*%>)', re.M, r'\3')
    END_ELSE_WITHOUT_WHITESPACE = aml.fixup(r'<%(!?)\s*end\s*%>\n(<%\1\s*else\s*%>)', None, r'\2')

    PRE_TRANSLATORS = [
        LINE_STATEMENT,
        LINE_EXPRESSION,
        PREPROCESSED_LINE_STATEMENT,
        PREPROCESSED_LINE_EXPRESSION,
        SELF_CLOSING_TAG,
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
        
        2. '% stmt' shortcut as a replacement for '<% stmt %>', and corresponding
           shpaml-style self-closing tag:
        
        % for post in @posts
            ...
        
        % >content_for :foo do
        
        3. '>tag' is equivalent to '> tag'.
        
        4. '= expression' is equivalent to '<%= expression %>'
        '''
        
        @shpaml.syntax(r'<% > *((\w+).*)')
        def SELF_CLOSING_TEMPLATE_STATEMENT(m):
            tag = m.group(1).strip()
            return '<%% %s<%% end %%>' % (m.group(1))
        
        shpaml.LINE_METHODS.insert(0, SELF_CLOSING_TEMPLATE_STATEMENT)
        
        TEMPLATE_STATEMENT = re.compile(r'<%(!?) (\w+)')
        
        def html_block_tag_with_template_statement(html_block_tag_without_template_statement, output, block, recurse):
            append = output.append
            prefix, tag = block[0]
            if shpaml.RAW_HTML.regex.match(tag):
                match = TEMPLATE_STATEMENT.match(tag)
                if match:
                    append(prefix + whitespace_removal.TextWithoutWhitespace(tag))
                    recurse(block[1:])
                    finalizer = '<%%%s end %%>' % match.group(1)
                    append(prefix + whitespace_removal.TextWithoutWhitespace(finalizer))
                    return
            html_block_tag_without_template_statement(output, block, recurse)
        
        runtime.hook_module_function(shpaml, 'html_block_tag', html_block_tag_with_template_statement)

aml.configure(ErbShortcuts)
convert_text = aml.convert_text

if __name__ == "__main__":
    import filter
    filter.perform_conversion(convert_text)
