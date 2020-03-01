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
    b'latin-1 = \xC3\xB0\n'
    b'bmp = \\u2603\n'
    b'astral = \\uD83D\\uDC10\n'
    b'bad-surrogate = \\uDC10\\uD83D\n'
)

@pytest.mark.parametrize('args,rc,output', [
    (
        ['select', '-', 'key'],
        0,
        b'key=value\n',
    ),
    (
        ['select', '-', 'nonexistent'],
        1,
        b'javaproperties select: nonexistent: key not found\n',
    ),
    (
        ['select', '-', 'key', 'nonexistent'],
        1,
        b'key=value\njavaproperties select: nonexistent: key not found\n',
    ),
    (
        ['select', '--escaped', '-', 'e\\u00F0'],
        0,
        b'e\\u00f0=escaped\n',
    ),
    (
        ['select', '--escaped', '--unicode', '-', 'e\\u00F0'],
        0,
        b'e\xF0=escaped\n',
    ),
    (
        ['select', '--escaped', '--unicode', '-EUTF-8', '-', 'e\\u00F0'],
        0,
        b'e\xC3\xB0=escaped\n',
    ),
    (
        ['select', '--escaped', '-', 'x\\u00F0'],
        1,
        b'javaproperties select: x\xC3\xB0: key not found\n'
    ),
    (
        ['select', '-', 'e\\u00f0'],
        0,
        b'e\\\\u00f0=not escaped\n',
    ),
    (
        ['select', '-', 'x\\u00f0'],
        1,
        b'javaproperties select: x\\u00f0: key not found\n'
    ),
    (
        ['select', '-', b'e\xC3\xB0'],
        0,
        b'e\\u00f0=escaped\n',
    ),
    (
        ['select', '--unicode', '-', b'e\xC3\xB0'],
        0,
        b'e\xF0=escaped\n',
    ),
    (
        ['select', '--unicode', '-EUTF-8', '-', b'e\xC3\xB0'],
        0,
        b'e\xC3\xB0=escaped\n',
    ),
    (
        ['select', '-', b'x\xC3\xB0'],
        1,
        b'javaproperties select: x\xC3\xB0: key not found\n',
    ),
    (
        ['select', '-', 'latin-1'],
        0,
        b'latin-1=\\u00c3\\u00b0\n',
    ),
    (
        ['select', '--ascii', '-', 'latin-1'],
        0,
        b'latin-1=\\u00c3\\u00b0\n',
    ),
    (
        ['select', '-EUTF-8', '-', 'latin-1'],
        0,
        b'latin-1=\\u00f0\n',
    ),
    (
        ['select', '--unicode', '-', 'latin-1'],
        0,
        b'latin-1=\xC3\xB0\n',
    ),
    (
        ['select', '-EUTF-8', '--unicode', '-', 'latin-1'],
        0,
        b'latin-1=\xC3\xB0\n',
    ),
    (
        ['select', '-', 'bmp'],
        0,
        b'bmp=\\u2603\n',
    ),
    (
        ['select', '--unicode', '-', 'bmp'],
        0,
        b'bmp=\\u2603\n',
    ),
    (
        ['select', '--unicode', '-EUTF-8', '-', 'bmp'],
        0,
        b'bmp=\xE2\x98\x83\n',
    ),
    (
        ['select', '-', 'astral'],
        0,
        b'astral=\\ud83d\\udc10\n'
    ),
    (
        ['select', '--unicode', '-EUTF-8', '-', 'astral'],
        0,
        b'astral=\xF0\x9F\x90\x90\n'
    ),
    (
        ['select', '-', 'bad-surrogate'],
        0,
        b'bad-surrogate=\\udc10\\ud83d\n',
    ),
    pytest.param(
        ['select', '--unicode', '-EUTF-8', '-', 'bad-surrogate'],
        0,
        b'bad-surrogate=\xED\xB0\x90\xED\xA0\xBD\n',
        marks=pytest.mark.skipif(
            sys.version_info[0] != 2,
            reason='Python 2 only',
        ),
    ),
    pytest.param(
        ['select', '--unicode', '-EUTF-8', '-', 'bad-surrogate'],
        0,
        b'bad-surrogate=\\udc10\\ud83d\n',
        marks=pytest.mark.skipif(
            sys.version_info[0] == 2,
            reason='Python 3 only',
        ),
    ),
])
def test_cmd_select(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == b'#Mon Nov 07 15:29:40 EST 2016\n' + output

# --outfile
# --separator
# -d
# -D
# universal newlines?
# getting a key that appears multiple times in the file
# getting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# invalid \u escape
