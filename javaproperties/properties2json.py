#!/usr/bin/python
import codecs
import io
import json
import sys
from   .reading import read_properties

# cf. <https://github.com/simplejson/simplejson/blob/master/simplejson/tool.py>

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        infile = io.open(sys.argv[1], 'rU', encoding='iso-8859-1')
    else:
        infile = sys.stdin
        if sys.version_info[0] >= 3:
            infile = infile.buffer
        ### TODO: Enable universal newlines mode
        infile = codecs.getreader('iso-8859-1')(infile)

    if len(sys.argv) > 2 and sys.argv[2] != "-":
        outfile = open(sys.argv[2], 'w')
    else:
        outfile = sys.stdout

    with infile, outfile:
        props = read_properties(infile)
        json.dump(props, outfile, sort_keys=True, indent=4,
                                  separators=(',', ': '))
        outfile.write('\n')

if __name__ == '__main__':
    main()
