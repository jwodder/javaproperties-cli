from   click.testing               import CliRunner
import pytest
from   javaproperties_cli.__main__ import javaproperties

INPUT = (
    b'foo: bar\n'
    b'key = value\n'
    b'zebra apple\n'
    b'e\\u00f0=escaped\n'
    b'e\\\\u00f0=not escaped\n'
    b'latin-1 = \xC3\xB0\n'
    b'bmp = \\u2603\n'
    b'astral = \\uD83D\\uDC10\n'
    b'bad-surrogate = \\uDC10\\uD83D\n'
)

@pytest.mark.parametrize('args,rc,output', [
    (
        ['get', '-', 'key'],
        0,
        b'value\n',
    ),
    (
        ['get', '-', 'nonexistent'],
        1,
        b'javaproperties get: nonexistent: key not found\n',
    ),
    (
        ['get', '--quiet', '-', 'nonexistent'],
        0,
        b'',
    ),
    (
        ['get', '-', 'key', 'nonexistent'],
        1,
        b'value\njavaproperties get: nonexistent: key not found\n',
    ),
    (
        ['get', '--quiet', '-', 'key', 'nonexistent'],
        0,
        b'value\n',
    ),
    (
        ['get', '-', '-d', '42', 'key'],
        0,
        b'value\n',
    ),
    (
        ['get', '-', '-d', '42', 'nonexistent'],
        0,
        b'42\n',
    ),
    (
        ['get', '-', '-d', '\\u7121', 'nonexistent'],
        0,
        b'\\u7121\n',
    ),
    (
        ['get', '-', '-d', '\\u7121', '--escaped', 'nonexistent'],
        0,
        b'\xE7\x84\xA1\n',
    ),
    (
        ['get', '--escaped', '-', 'e\\u00F0'],
        0,
        b'escaped\n',
    ),
    (
        ['get', '--escaped', '-', 'x\\u00F0'],
        1,
        b'javaproperties get: x\xC3\xB0: key not found\n',
    ),
    (
        ['get', '-', 'e\\u00f0'],
        0,
        b'not escaped\n',
    ),
    (
        ['get', '-', 'x\\u00f0'],
        1,
        b'javaproperties get: x\\u00f0: key not found\n',
    ),
    (
        ['get', '-', b'e\xC3\xB0'],
        0,
        b'escaped\n',
    ),
    (
        ['get', '-', b'x\xC3\xB0'],
        1,
        b'javaproperties get: x\xC3\xB0: key not found\n',
    ),
    (
        ['get', '-', 'latin-1'],
        0,
        b'\xC3\x83\xC2\xB0\n',
    ),
    (
        ['get', '--encoding=utf-8', '-', 'latin-1'],
        0,
        b'\xC3\xB0\n',
    ),
    (
        ['get', '-', 'bmp'],
        0,
        b'\xE2\x98\x83\n',
    ),
    (
        ['get', '-', 'astral'],
        0,
        b'\xF0\x9F\x90\x90\n',
    ),
    pytest.param(
        ['get', '-', 'bad-surrogate'],
        0,
        b'??\n',
        marks=[
            pytest.mark.xfail(reason='https://github.com/pallets/click/issues/705'),
        ],
    ),
    (
        ['get', '-', 'key', 'key'],
        0,
        b'value\nvalue\n'
    ),
    (
        ['get', '-', 'foo', 'zebra'],
        0,
        b'bar\napple\n'
    ),
    (
        ['get', '-', 'zebra', 'foo'],
        0,
        b'apple\nbar\n'
    ),
])
def test_cmd_get(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_get_repeated():
    r = CliRunner().invoke(
        javaproperties,
        ['get', '-', 'repeated'],
        input=(
            b'foo: bar\n'
            b'repeated = first\n'
            b'key = value\n'
            b'zebra apple\n'
            b'repeated = second\n'
        ),
    )
    assert r.exit_code == 0, r.stdout_bytes
    assert r.stdout_bytes == b'second\n'

@pytest.mark.parametrize('args,rc,output', [
    (
        ['get', '--defaults', 'defaults.properties', '-', 'key'],
        0,
        b'value\n',
    ),
    (
        ['get', '--defaults', 'defaults.properties', '-', 'lost'],
        0,
        b'found\n',
    ),
    (
        ['get', '--defaults', 'defaults.properties', '-', 'nonexistent'],
        1,
        b'javaproperties get: nonexistent: key not found\n',
    ),
    (
        ['get', '-q', '--defaults', 'defaults.properties', '-', 'nonexistent'],
        0,
        b'',
    ),
    (
        ['get', '-D', 'defaults.properties', '-d42', '-', 'key'],
        0,
        b'value\n',
    ),
    (
        ['get', '-D', 'defaults.properties', '-d42', '-', 'lost'],
        0,
        b'found\n',
    ),
    (
        ['get', '-D', 'defaults.properties', '-d42', '-', 'nonexistent'],
        0,
        b'42\n',
    ),
])
def test_cmd_get_with_defaults(defaults_file, args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

# universal newlines?
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# invalid \u escape
