from   click.testing               import CliRunner
import pytest
from   javaproperties_cli.fromjson import json2properties

TOPLEVEL_ERRMSG = b'''\
Usage: json2properties [OPTIONS] [INFILE] [OUTFILE]
Try "json2properties -h" for help.

Error: Only dicts can be converted to .properties
'''

BADVAL_ERRMSG = b'''\
Usage: json2properties [OPTIONS] [INFILE] [OUTFILE]
Try "json2properties -h" for help.

Error: Dictionary values must be scalars, not lists or dicts
'''

@pytest.mark.parametrize('args,inp,success,output', [
    (
        [],
        b'{}',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n',
    ),
    (
        [],
        b'{\n'
        b'    "key": "value",\n'
        b'    "foo": "bar",\n'
        b'    "zebra": "apple"\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo=bar\n'
        b'key=value\n'
        b'zebra=apple\n',
    ),
    (
        [],
        b'{\n'
        b'    "yes": true,\n'
        b'    "no": false,\n'
        b'    "nothing": null,\n'
        b'    "answer": 42\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'answer=42\n'
        b'no=false\n'
        b'nothing=null\n'
        b'yes=true\n',
    ),
    (
        [],
        b'{\n'
        b'    "pi": 3.14159265358979323846264338327950288419716939937510582097494459\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'pi=3.14159265358979323846264338327950288419716939937510582097494459\n'
    ),
    (
        [],
        b'[{\n'
        b'    "key": "value",\n'
        b'    "foo": "bar",\n'
        b'    "zebra": "apple"\n'
        b'}]\n',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        br'"{\"key\": \"value\", \"foo\": \"bar\", \"zebra\": \"apple\"}"',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        b'42\n',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        b'3.14\n',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        b'true\n',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        b'null\n',
        False,
        TOPLEVEL_ERRMSG,
    ),
    (
        [],
        b'{\n'
        b'    "list": [1, 2, 3],\n'
        b'    "foo": "bar"\n'
        b'}\n',
        False,
        BADVAL_ERRMSG,
    ),
    (
        [],
        b'{\n'
        b'    "map": {"bar": "foo"},\n'
        b'    "foo": "bar"\n'
        b'}\n',
        False,
        BADVAL_ERRMSG,
    ),
    (
        [],
        b'{\n'
        b'    "edh": "\\u00F0",\n'
        b'    "snowman": "\\u2603",\n'
        b'    "goat": "\\uD83D\\uDC10",\n'
        b'    "\\u00F0": "edh",\n'
        b'    "\\u2603": "snowman",\n'
        b'    "\\uD83D\\uDC10": "goat"\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh=\\u00f0\n'
        b'goat=\\ud83d\\udc10\n'
        b'snowman=\\u2603\n'
        b'\\u00f0=edh\n'
        b'\\u2603=snowman\n'
        b'\\ud83d\\udc10=goat\n',
    ),
    (
        [],
        b'{\n'
        b'    "edh": "\xC3\xB0",\n'
        b'    "snowman": "\xE2\x98\x83",\n'
        b'    "goat": "\xF0\x9F\x90\x90",\n'
        b'    "\xC3\xB0": "edh",\n'
        b'    "\xE2\x98\x83": "snowman",\n'
        b'    "\xF0\x9F\x90\x90": "goat"\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh=\\u00f0\n'
        b'goat=\\ud83d\\udc10\n'
        b'snowman=\\u2603\n'
        b'\\u00f0=edh\n'
        b'\\u2603=snowman\n'
        b'\\ud83d\\udc10=goat\n',
    ),
    (
        ['-s\t:  '],
        b'{\n'
        b'    "key": "value",\n'
        b'    "foo": "bar",\n'
        b'    "zebra": "apple"\n'
        b'}\n',
        True,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo\t:  bar\n'
        b'key\t:  value\n'
        b'zebra\t:  apple\n',
    ),
    (
        ['-c', 'This is a comment.'],
        b'{\n'
        b'    "key": "value",\n'
        b'    "foo": "bar",\n'
        b'    "zebra": "apple"\n'
        b'}\n',
        True,
        b'#This is a comment.\n'
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo=bar\n'
        b'key=value\n'
        b'zebra=apple\n',
    ),
])
def test_json2properties(args, inp, success, output):
    r = CliRunner().invoke(json2properties, args, input=inp)
    if success:
        assert r.exit_code == 0
    else:
        assert r.exit_code != 0
    assert r.stdout_bytes == output

# invalid JSON
# UTF-16 input
# Latin-1 input? (treated as invalid UTF-8 by `json.load`?)
# Test with actual files as infile & outfile
