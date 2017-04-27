from   click.testing               import CliRunner
from   freezegun                   import freeze_time
from   javaproperties_cli.fromjson import json2properties

TOPLEVEL_ERRMSG = b'''\
Usage: json2properties [OPTIONS] [INFILE] [OUTFILE]

Error: Only dicts can be converted to .properties
'''

BADVAL_ERRMSG = b'''\
Usage: json2properties [OPTIONS] [INFILE] [OUTFILE]

Error: Dictionary values must be scalars, not lists or dicts
'''

@freeze_time('2016-11-07 20:29:40')
def test_json2properties_empty():
    r = CliRunner().invoke(json2properties, input=b'{}')
    assert r.exit_code == 0
    assert r.output_bytes == b'#Mon Nov 07 15:29:40 EST 2016\n'

@freeze_time('2016-11-07 20:29:40')
def test_json2properties_simple():
    r = CliRunner().invoke(json2properties, input=b'''{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
foo=bar
key=value
zebra=apple
'''

@freeze_time('2016-11-07 20:29:40')
def test_json2properties_nonstring():
    r = CliRunner().invoke(json2properties, input=b'''{
        "yes": true,
        "no": false,
        "nothing": null,
        "answer": 42
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
answer=42
no=false
nothing=null
yes=true
'''

@freeze_time('2016-11-07 20:29:40')
def test_json2properties_float():
    r = CliRunner().invoke(json2properties, input=b'''{
        "pi": 3.14159265358979323846264338327950288419716939937510582097494459
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
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
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_string():
    r = CliRunner().invoke(
        json2properties,
        input=br'"{\"key\": \"value\", \"foo\": \"bar\", \"zebra\": \"apple\"}"'
    )
    assert r.exit_code != 0
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_int():
    r = CliRunner().invoke(json2properties, input=b'42\n')
    assert r.exit_code != 0
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_float():
    r = CliRunner().invoke(json2properties, input=b'3.14\n')
    assert r.exit_code != 0
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_true():
    r = CliRunner().invoke(json2properties, input=b'true\n')
    assert r.exit_code != 0
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_toplevel_null():
    r = CliRunner().invoke(json2properties, input=b'null\n')
    assert r.exit_code != 0
    assert r.output_bytes == TOPLEVEL_ERRMSG

def test_json2properties_array_val():
    r = CliRunner().invoke(json2properties, input=b'''{
        "list": [1, 2, 3],
        "foo": "bar"
    }''')
    assert r.exit_code != 0
    assert r.output_bytes == BADVAL_ERRMSG

def test_json2properties_dict_val():
    r = CliRunner().invoke(json2properties, input=b'''{
        "map": {"bar": "foo"},
        "foo": "bar"
    }''')
    assert r.exit_code != 0
    assert r.output_bytes == BADVAL_ERRMSG

# non-ASCII characters (escaped & unescaped in input)
# --separator
# invalid JSON
