HTML_COMMENT_SYNTAX = '<!-- %s -->'

def parse_arguments():
    ''' Parses options and arguments for filter scripts.
    
    Without arguments, converts stdin to stdout.
    With a single argument converts specified filename to stdout,
    unless filename is - in which case stdin is converted.
    Accepts one option, -o output-file which causes output
    to be written to output-file instead of stdout.
    
    Returns a tuple (input, output) where input is None
    to use standard input or file name, and output is None
    to use standard output or file name.
    '''
    
    import optparse
    
    usage = 'Usage: %prog [options] [input-file]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--output', metavar='FILE',
        help='Write output to FILE')
    parser.add_option('-g', '--generated-warning', action='store_true',
        help='Add generated file warning to output')
    parser.add_option('-c', '--comment-syntax', metavar='FORMAT',
        help='Comment syntax to use (e.g. "<!-- %s -->" for HTML comments, which is the default). %s will be replaced with comment text. Literal percent signs should be doubled like so: %%')
    
    options, args = parser.parse_args()
    
    # if file name is given convert file, else convert stdin.
    # - is alias for stdin.
    if len(args) == 1:
        input = args[0]
        if input == '-':
            input = None
    elif len(args) == 0:
        input = None
    else:
        parser.print_help()
        exit(2)
    
    # allow - as alias for stdout.
    output = options.output
    if output == '-':
        output = None
    
    return (input, output, options)

def perform_conversion(convert_func, forward_arguments=False, pass_input_name=False):
    ''' Converts text in input file or standard input using
    convert_func and writes results to output file or
    standard output as specified by program options.
    
    Options are parsed with parse_arguments.
    
    If forward_arguments is False (default), convert_func
    should be a function accepting a single string argument
    and returning a string.
    
    If forward_arguments is True, convert_func should be a
    function accepting a string positional argument and
    input and output keyword arguments. input and output
    will be set to None or file names if provided by user.
    
    If pass_input_name is True, input file is not opened.
    Instead its name (either None for standard input or
    file name or path specified by user) is given to
    convert_func. If forward_arguments is True, convert_func
    is also given an output keyword argument.
    '''
    
    import sys
    
    input, output, options = parse_arguments()
    
    if pass_input_name:
        if forward_arguments:
            output_text = convert_func(input, output=output)
        else:
            output_text = convert_func(input)
    else:
        if input is None:
            input_text = sys.stdin.read()
        else:
            f = open(input)
            try:
                input_text = f.read()
            finally:
                f.close()
        
        if forward_arguments:
            output_text = convert_func(input_text, input=input, output=output)
        else:
            output_text = convert_func(input_text)
    
    assert output_text, "convert_func did not return anything to perform_conversion"
    
    if options.generated_warning:
        comment_syntax = options.comment_syntax or HTML_COMMENT_SYNTAX
        warning = comment_syntax % 'Generated file - DO NOT EDIT' + "\n"
        if input is not None:
            warning += comment_syntax % ('Created from: %s' % input) + "\n"
        output_text = warning + output_text
    
    if output is None:
        sys.stdout.write(output_text)
    else:
        f = open(output, 'w')
        try:
            f.write(output_text)
        finally:
            f.close()
