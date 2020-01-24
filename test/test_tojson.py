from   click.testing             import CliRunner
from   javaproperties_cli.tojson import properties2json

def test_properties2json_empty():
    r = CliRunner().invoke(properties2json, input=b'')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'{}\n'

def test_properties2json_comment_only():
    r = CliRunner().invoke(properties2json, input=b'#This is a comment.\n')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'{}\n'

def test_properties2json_simple():
    r = CliRunner().invoke(properties2json, input=b'''
#Mon Nov 07 15:29:40 EST 2016
key = value
foo: bar
zebra apple
''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
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
    assert r.stdout_bytes == b'''{
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
    assert r.stdout_bytes == b'''{
    "empty": "",
    "missing": ""
}
'''

def test_properties2json_escaped_nonascii_input():
    r = CliRunner().invoke(properties2json, input=b'''
#Mon Nov 07 15:29:40 EST 2016
edh: \\u00F0
snowman: \\u2603
goat: \\uD83D\\uDC10
\\u00F0: edh
\\uD83D\\uDC10: goat
\\u2603: snowman
''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
    "edh": "\\u00f0",
    "goat": "\\ud83d\\udc10",
    "snowman": "\\u2603",
    "\\u00f0": "edh",
    "\\u2603": "snowman",
    "\\ud83d\\udc10": "goat"
}
'''

def test_properties2json_utf8_input_no_encoding():
    r = CliRunner().invoke(properties2json, input=b'''
#Mon Nov 07 15:29:40 EST 2016
edh: \xC3\xB0
snowman: \xE2\x98\x83
goat: \xF0\x9F\x90\x90
\xC3\xB0: edh
\xF0\x9F\x90\x90: goat
\xE2\x98\x83: snowman
''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
    "edh": "\\u00c3\\u00b0",
    "goat": "\\u00f0\\u009f\\u0090\\u0090",
    "snowman": "\\u00e2\\u0098\\u0083",
    "\\u00c3\\u00b0": "edh",
    "\\u00e2\\u0098\\u0083": "snowman",
    "\\u00f0\\u009f\\u0090\\u0090": "goat"
}
'''

def test_properties2json_utf8_input():
    r = CliRunner().invoke(properties2json, ['--encoding', 'utf-8'], input=b'''
#Mon Nov 07 15:29:40 EST 2016
edh: \xC3\xB0
snowman: \xE2\x98\x83
goat: \xF0\x9F\x90\x90
\xC3\xB0: edh
\xF0\x9F\x90\x90: goat
\xE2\x98\x83: snowman
''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
    "edh": "\\u00f0",
    "goat": "\\ud83d\\udc10",
    "snowman": "\\u2603",
    "\\u00f0": "edh",
    "\\u2603": "snowman",
    "\\ud83d\\udc10": "goat"
}
'''

def test_properties2json_utf16_input():
    r = CliRunner().invoke(properties2json, ['--encoding', 'utf-16BE'], input=u'''
#Mon Nov 07 15:29:40 EST 2016
edh: \u00F0
snowman: \u2603
goat: \U0001F410
\u00F0: edh
\U0001F410: goat
\u2603: snowman
'''.encode('UTF-16BE'))
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
    "edh": "\\u00f0",
    "goat": "\\ud83d\\udc10",
    "snowman": "\\u2603",
    "\\u00f0": "edh",
    "\\u2603": "snowman",
    "\\ud83d\\udc10": "goat"
}
'''

def test_properties2json_repeated_key():
    r = CliRunner().invoke(properties2json, input=b'''
#Mon Nov 07 15:29:40 EST 2016
key = value
foo: bar
zebra apple
key=lock
''')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''{
    "foo": "bar",
    "key": "lock",
    "zebra": "apple"
}
'''

# invalid \u escape
# Test with actual files as infile & outfile
