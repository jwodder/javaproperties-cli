from   click.testing               import CliRunner
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

def test_json2properties_empty():
    r = CliRunner().invoke(json2properties, input=b'{}')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'#Mon Nov 07 15:29:40 EST 2016\n'

def test_json2properties_simple():
    r = CliRunner().invoke(json2properties, input=b'''{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
foo=bar
key=value
zebra=apple
'''

def test_json2properties_nonstring():
    r = CliRunner().invoke(json2properties, input=b'''{
        "yes": true,
        "no": false,
        "nothing": null,
        "answer": 42
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
answer=42
no=false
nothing=null
yes=true
'''

def test_json2properties_float():
    r = CliRunner().invoke(json2properties, input=b'''{
        "pi": 3.14159265358979323846264338327950288419716939937510582097494459
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
pi=3.14159265358979323846264338327950288419716939937510582097494459
'''

def test_json2properties_toplevel_array():
    r = CliRunner().invoke(json2properties, input=b'''[{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }]''')
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_string():
    r = CliRunner().invoke(
        json2properties,
        input=br'"{\"key\": \"value\", \"foo\": \"bar\", \"zebra\": \"apple\"}"'
    )
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_int():
    r = CliRunner().invoke(json2properties, input=b'42\n')
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_float():
    r = CliRunner().invoke(json2properties, input=b'3.14\n')
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_true():
    r = CliRunner().invoke(json2properties, input=b'true\n')
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_null():
    r = CliRunner().invoke(json2properties, input=b'null\n')
    assert r.exit_code != 0
    assert r.stdout_bytes == TOPLEVEL_ERRMSG

def test_json2properties_array_val():
    r = CliRunner().invoke(json2properties, input=b'''{
        "list": [1, 2, 3],
        "foo": "bar"
    }''')
    assert r.exit_code != 0
    assert r.stdout_bytes == BADVAL_ERRMSG

def test_json2properties_dict_val():
    r = CliRunner().invoke(json2properties, input=b'''{
        "map": {"bar": "foo"},
        "foo": "bar"
    }''')
    assert r.exit_code != 0
    assert r.stdout_bytes == BADVAL_ERRMSG

def test_json2properties_escaped_nonascii_input():
    r = CliRunner().invoke(json2properties, input=b'''{
        "edh": "\\u00F0",
        "snowman": "\\u2603",
        "goat": "\\uD83D\\uDC10",
        "\\u00F0": "edh",
        "\\u2603": "snowman",
        "\\uD83D\\uDC10": "goat"
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
edh=\\u00f0
goat=\\ud83d\\udc10
snowman=\\u2603
\\u00f0=edh
\\u2603=snowman
\\ud83d\\udc10=goat
'''

def test_json2properties_utf8_input():
    r = CliRunner().invoke(json2properties, input=b'''{
        "edh": "\xC3\xB0",
        "snowman": "\xE2\x98\x83",
        "goat": "\xF0\x9F\x90\x90",
        "\xC3\xB0": "edh",
        "\xE2\x98\x83": "snowman",
        "\xF0\x9F\x90\x90": "goat"
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
edh=\\u00f0
goat=\\ud83d\\udc10
snowman=\\u2603
\\u00f0=edh
\\u2603=snowman
\\ud83d\\udc10=goat
'''

def test_json2properties_separator():
    r = CliRunner().invoke(json2properties, ['-s\t:  '], input=b'''{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
foo\t:  bar
key\t:  value
zebra\t:  apple
'''

def test_json2properties_comment():
    r = CliRunner().invoke(json2properties, ['-c', 'This is a comment.'],
                           input=b'''{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#This is a comment.
#Mon Nov 07 15:29:40 EST 2016
foo=bar
key=value
zebra=apple
'''

# invalid JSON (This includes invalid surrogate pairs in Python 2.6 but not in
# other versions)
# UTF-16 input
# Latin-1 input? (treated as invalid UTF-8 by `json.load`?)
# Test with actual files as infile & outfile
