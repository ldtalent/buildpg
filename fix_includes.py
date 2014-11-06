import sys

jade_fn = sys.argv[1]
#print 'ARGV: '
#print sys.argv
if len(sys.argv) > 2:
    is_in_partial = True
else:
    is_in_partial = False
print 'is_in_partial: '
print is_in_partial
print 'fixing includes in ' + jade_fn

to_unindent = []
to_unindent_threshold = []

jade_f = open(jade_fn)
new_jade_f = open(jade_fn + '.new', 'w')
for line in jade_f:
    full_line = line
    line_str = full_line.strip()
    line_arr = line_str.split(' ')
    if len(line_arr) == 2 and line_arr[0] == 'include':
        include = line_arr[1]
        include_arr = include.split('/')
        if len(include_arr) == 0:
            print 'ERROR: included empty file path'
        if len(include_arr) == 1 or is_in_partial or include_arr[-2] != 'partials':
            new_include = include_arr[-1]
        else:
            new_include = '/'.join(include_arr[-2:])
        new_line_str = 'include ' + new_include
        full_line = full_line.replace(line_str, new_line_str)
    
    # handle indentation changes due to logic removals
    indent = len(full_line) - len(full_line.lstrip(' '))
    print '---------'
    print 'full_line: ' + str(full_line)
    print 'indent: ' + str(indent)

    for thresh in reversed(to_unindent_threshold):
        if (indent < thresh):
            to_unindent_threshold.pop()
            to_unindent.pop()

    print 'to_unindent: ' + str(to_unindent)
    print 'to_unindent_threshold: ' + str(to_unindent_threshold)

    full_line = full_line[sum(to_unindent):]

    # remove logic - http://jade-lang.com/reference/
    # note the following would cause some extra indentation on inner blocks, but jade seems to be lenient on it (install jade version 1.7.0 globally)
    if len(line_arr) > 1 and line_arr[0] == '-':
        full_line = ''
    if len(line_arr) > 1 and line_arr[0] == 'case':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) == 1 and line_arr[0] == 'default':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'if':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'else':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'elif': 
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'unless':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'each':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'while':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if len(line_arr) > 1 and line_arr[0] == 'for':
        full_line = ''
        to_unindent.append(2)
        to_unindent_threshold.append(indent + 2)
    if line_arr[0] == '//':
        full_line = ''

    new_jade_f.write(full_line)

jade_f.close()
