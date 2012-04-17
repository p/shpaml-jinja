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

import re

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

class NotConfiguredError(ValueError):
    ''' Raised when attempting to convert text with aml without first
    choosing template engine and whitespace removal options.'''

class AlreadyConfiguredError(ValueError):
    ''' Raised when attempting to configure aml more than once per process.
    
    Since aml runtime-patches shpaml, a single process may have only one
    aml configuration.
    '''

def configure(template_engine, remove_whitespace=True):
    if configuration.configured:
        raise AlreadyConfiguredError
    
    template_engine.install()
    configuration.active_shortcuts = template_engine
    
    if remove_whitespace:
        import whitespace_removal
        whitespace_removal.WhitespaceRemoval.install()
        configuration.active_shortcuts.POST_TRANSLATORS = \
            configuration.active_shortcuts.POST_TRANSLATORS_WITHOUT_WHITESPACE
    
    configuration.configured = True

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
    
    if not configuration.configured:
        raise NotConfiguredError
    
    text = configuration.active_shortcuts.convert_text_pre(text)
    text = shpaml.convert_text(text)
    text = configuration.active_shortcuts.convert_text_post(text)
    return text

# Only implementation is beyond this point.

class Configuration:
    def __init__(self):
        self.configured = False
        self.active_shortcuts = None

configuration = Configuration()

TAB_INDENT = re.compile(r'^ *\t', re.M)
LINE_CONTINUATION = re.compile(r'\\$\n\s*', re.M)

def fixup(regex, flags, replacement):
    if flags is not None:
        options = [flags]
    else:
        options = []
    regex = re.compile(regex, *options)
    return (regex, replacement)

class ShortcutsBase:
    active_post_translators = None
    
    @classmethod
    def convert_text_pre(cls, text):
        ''' Performs pre-processing pass on text before handing it off to shpaml.
        
        First, indentation is checked and if tabs are used for indentation
        IndentError is raised.
        
        Then, jinja shortcuts in text are replaced with expanded equivalents.
        '''
        
        if TAB_INDENT.search(text):
            raise IndentError('Text uses tabs for indentation')
        
        text = LINE_CONTINUATION.sub('', text)
        
        for translator in cls.PRE_TRANSLATORS:
            text = translator[0].sub(translator[1], text)
        
        return text
    
    @classmethod
    def convert_text_post(cls, text):
        ''' Performs post-processing pass on text after it is processed by shpaml.
        
        Post-processing fixes up things like if/endif/else/endelse into if/else/endif.'
        '''
        
        for translator in cls.POST_TRANSLATORS:
            text = translator[0].sub(translator[1], text)
        
        return text
