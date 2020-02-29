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
)

@pytest.mark.parametrize('args,rc,output', [
    (
        ['delete', '--preserve-timestamp', '-', 'key'],
        0,
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '-', 'nonexistent'],
        0,
        INPUT,
    ),
    (
        ['delete', '--preserve-timestamp', '-', 'key', 'nonexistent'],
        0,
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '--escaped', '-', 'e\\u00F0'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '--escaped', '-', 'x\\u00F0'],
        0,
        INPUT,
    ),
    (
        ['delete', '--preserve-timestamp', '-', 'e\\u00f0'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '-', 'x\\u00f0'],
        0,
        INPUT,
    ),
    (
        ['delete', '--preserve-timestamp', '-', b'e\xC3\xB0'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '-', b'x\xC3\xB0'],
        0,
        INPUT,
    ),
])
def test_cmd_delete(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_delete_del_bad_surrogate():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'bad-surrogate'
    ], input=b'good-surrogate = \\uD83D\\uDC10\n'
             b'bad-surrogate = \\uDC10\\uD83D\n')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'good-surrogate = \\uD83D\\uDC10\n'

def test_cmd_delete_keep_bad_surrogate():
    r = CliRunner().invoke(javaproperties, [
        'delete', '--preserve-timestamp', '-', 'good-surrogate'
    ], input=b'good-surrogate = \\uD83D\\uDC10\n'
             b'bad-surrogate = \\uDC10\\uD83D\n')
    assert r.exit_code == 0
    assert r.stdout_bytes == b'bad-surrogate = \\uDC10\\uD83D\n'

# --encoding
# --outfile
# --preserve-timestamp when there is a timestamp in input
# no --preserve-timestamp, with & without a timestamp in input
# stripping extra trailing line continuations
# universal newlines?
# deleting a key that appears multiple times in the file
# deleting keys out of order
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# invalid \u escape
