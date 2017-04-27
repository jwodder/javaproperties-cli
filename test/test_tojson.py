from   click.testing             import CliRunner
from   javaproperties_cli.tojson import properties2json

def test_properties2json_empty():
    r = CliRunner().invoke(properties2json, input=b'')
    assert r.exit_code == 0
    assert r.output_bytes == b'{}\n'

def test_properties2json_comment_only():
    r = CliRunner().invoke(properties2json, input=b'#This is a comment.\n')
    assert r.exit_code == 0
    assert r.output_bytes == b'{}\n'

def test_properties2json_simple():
    r = CliRunner().invoke(properties2json, input=b'''
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

def test_properties2json_scalarlike():
    r = CliRunner().invoke(properties2json, input=b'''
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

def test_properties2json_empty_value():
    r = CliRunner().invoke(properties2json, input=b'''
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
