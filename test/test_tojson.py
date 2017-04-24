from   click.testing             import CliRunner
from   javaproperties_cli.tojson import tojson

def test_tojson_empty():
    r = CliRunner().invoke(tojson, input=b'')
    assert r.exit_code == 0
    assert r.output_bytes == b'{}\n'

def test_tojson_comment_only():
    r = CliRunner().invoke(tojson, input=b'#This is a comment.\n')
    assert r.exit_code == 0
    assert r.output_bytes == b'{}\n'

def test_tojson_simple():
    r = CliRunner().invoke(tojson, input=b'''
#Mon Nov 07 15:29:40 EST 2016
key = value
foo: bar
zebra apple
''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''{
    "foo": "bar",
    "key": "value",
    "zebra": "apple"
}
'''

def test_tojson_scalarlike():
    r = CliRunner().invoke(tojson, input=b'''
#Mon Nov 07 15:29:40 EST 2016
key = 42
foo: 3.14
zebra null
true=false
''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''{
    "foo": "3.14",
    "key": "42",
    "true": "false",
    "zebra": "null"
}
'''

def test_tojson_empty_value():
    r = CliRunner().invoke(tojson, input=b'''
#Mon Nov 07 15:29:40 EST 2016
empty=
missing
''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''{
    "empty": "",
    "missing": ""
}
'''

# repeated keys?
# non-ASCII characters
# --encoding
