from   click.testing             import CliRunner
import pytest
from   javaproperties_cli.tojson import properties2json

@pytest.mark.parametrize('args,inp,success,output', [
    (
        [],
        b'',
        True,
        b'{}\n',
    ),
    (
        [],
        b'#This is a comment.\n',
        True,
        b'{}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'key = value\n'
        b'foo: bar\n'
        b'zebra apple\n',
        True,
        b'{\n'
        b'    "foo": "bar",\n'
        b'    "key": "value",\n'
        b'    "zebra": "apple"\n'
        b'}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'key = 42\n'
        b'foo: 3.14\n'
        b'zebra null\n'
        b'true=false\n',
        True,
        b'{\n'
        b'    "foo": "3.14",\n'
        b'    "key": "42",\n'
        b'    "true": "false",\n'
        b'    "zebra": "null"\n'
        b'}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'empty=\n'
        b'missing\n',
        True,
        b'{\n'
        b'    "empty": "",\n'
        b'    "missing": ""\n'
        b'}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh: \\u00F0\n'
        b'snowman: \\u2603\n'
        b'goat: \\uD83D\\uDC10\n'
        b'\\u00F0: edh\n'
        b'\\uD83D\\uDC10: goat\n'
        b'\\u2603: snowman\n',
        True,
        b'{\n'
        b'    "edh": "\\u00f0",\n'
        b'    "goat": "\\ud83d\\udc10",\n'
        b'    "snowman": "\\u2603",\n'
        b'    "\\u00f0": "edh",\n'
        b'    "\\u2603": "snowman",\n'
        b'    "\\ud83d\\udc10": "goat"\n'
        b'}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh: \xC3\xB0\n'
        b'snowman: \xE2\x98\x83\n'
        b'goat: \xF0\x9F\x90\x90\n'
        b'\xC3\xB0: edh\n'
        b'\xF0\x9F\x90\x90: goat\n'
        b'\xE2\x98\x83: snowman\n',
        True,
        b'{\n'
        b'    "edh": "\\u00c3\\u00b0",\n'
        b'    "goat": "\\u00f0\\u009f\\u0090\\u0090",\n'
        b'    "snowman": "\\u00e2\\u0098\\u0083",\n'
        b'    "\\u00c3\\u00b0": "edh",\n'
        b'    "\\u00e2\\u0098\\u0083": "snowman",\n'
        b'    "\\u00f0\\u009f\\u0090\\u0090": "goat"\n'
        b'}\n',
    ),
    (
        ['--encoding', 'utf-8'],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh: \xC3\xB0\n'
        b'snowman: \xE2\x98\x83\n'
        b'goat: \xF0\x9F\x90\x90\n'
        b'\xC3\xB0: edh\n'
        b'\xF0\x9F\x90\x90: goat\n'
        b'\xE2\x98\x83: snowman\n',
        True,
        b'{\n'
        b'    "edh": "\\u00f0",\n'
        b'    "goat": "\\ud83d\\udc10",\n'
        b'    "snowman": "\\u2603",\n'
        b'    "\\u00f0": "edh",\n'
        b'    "\\u2603": "snowman",\n'
        b'    "\\ud83d\\udc10": "goat"\n'
        b'}\n',
    ),
    (
        ['--encoding', 'utf-8', '--unicode'],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'edh: \xC3\xB0\n'
        b'snowman: \xE2\x98\x83\n'
        b'goat: \xF0\x9F\x90\x90\n'
        b'\xC3\xB0: edh\n'
        b'\xF0\x9F\x90\x90: goat\n'
        b'\xE2\x98\x83: snowman\n',
        True,
        b'{\n'
        b'    "edh": "\xC3\xB0",\n'
        b'    "goat": "\xF0\x9F\x90\x90",\n'
        b'    "snowman": "\xE2\x98\x83",\n'
        b'    "\xC3\xB0": "edh",\n'
        b'    "\xE2\x98\x83": "snowman",\n'
        b'    "\xF0\x9F\x90\x90": "goat"\n'
        b'}\n',
    ),
    (
        ['--encoding', 'utf-16BE'],
        u'#Mon Nov 07 15:29:40 EST 2016\n'
        u'edh: \u00F0\n'
        u'snowman: \u2603\n'
        u'goat: \U0001F410\n'
        u'\u00F0: edh\n'
        u'\U0001F410: goat\n'
        u'\u2603: snowman\n'.encode('UTF-16BE'),
        True,
        b'{\n'
        b'    "edh": "\\u00f0",\n'
        b'    "goat": "\\ud83d\\udc10",\n'
        b'    "snowman": "\\u2603",\n'
        b'    "\\u00f0": "edh",\n'
        b'    "\\u2603": "snowman",\n'
        b'    "\\ud83d\\udc10": "goat"\n'
        b'}\n',
    ),
    (
        [],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'key = value\n'
        b'foo: bar\n'
        b'zebra apple\n'
        b'key=lock\n',
        True,
        b'{\n'
        b'    "foo": "bar",\n'
        b'    "key": "lock",\n'
        b'    "zebra": "apple"\n'
        b'}\n',
    ),
])
def test_properties2json(args, inp, success, output):
    r = CliRunner().invoke(properties2json, args, input=inp)
    if success:
        assert r.exit_code == 0
    else:
        assert r.exit_code != 0
    assert r.stdout_bytes == output

# invalid \u escape
# Test with actual files as infile & outfile
# Test that UTF-8 is still emitted when LC_ALL is not a UTF-8 locale
