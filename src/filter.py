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
    parser.add_option('-o', '--output', dest='output', help='Write output to FILE', metavar='FILE')
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
    
    return (input, output)

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
    
    input, output = parse_arguments()
    
    if pass_input_name:
        if forward_arguments:
            output_text = convert_func(input, output=output)
        else:
            output_text = convert_func(input)
    else:
        if input is None:
            input_text = sys.stdin.read()
        else:
            with open(input) as f:
                input_text = f.read()
        
        if forward_arguments:
            output_text = convert_func(input_text, input=input, output=output)
        else:
            output_text = convert_func(input_text)
    
    assert output_text, "convert_func did not return anything to perform_conversion"
    
    if output is None:
        sys.stdout.write(output_text)
    else:
        with open(output, 'w') as f:
            f.write(output_text)
