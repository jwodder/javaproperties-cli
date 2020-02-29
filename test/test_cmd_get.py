import sys
from   click.testing               import CliRunner
import pytest
from   javaproperties_cli.__main__ import javaproperties

INPUT = (
    b'foo: bar\n'
    b'key = value\n'
    b'zebra apple\n'
    b'e\\u00f0=escaped\n'
    b'e\\\\u00f0=not escaped\n'
    b'latin-1 = \xF0\n'
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
        ['get', '-', 'key', 'nonexistent'],
        1,
        b'value\njavaproperties get: nonexistent: key not found\n',
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
        b'\xED\xB0\x90\xED\xA0\xBD\n',
        marks=pytest.mark.skipif(
            sys.version_info[0] != 2,
            reason='Python 2 only',
        ),
    ),
    pytest.param(
        ['get', '-', 'bad-surrogate'],
        0,
        b'??\n',
        marks=[
            pytest.mark.xfail(reason='https://github.com/pallets/click/issues/705'),
            pytest.mark.skipif(
                sys.version_info[0] < 3,
                reason='Python 3 only',
            ),
        ],
    ),
])
def test_cmd_get(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

# --encoding
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# invalid \u escape
