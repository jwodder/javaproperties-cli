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
        ['set', '--preserve-timestamp', '-', 'key', 'other value'],
        0,
        b'foo: bar\n'
        b'key=other value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        ['set', '--preserve-timestamp', '-', 'nonexistent', 'mu'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'nonexistent=mu\n',
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '-',
            'e\\u00F0', '\\u00A1new!',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=\\u00a1new\\!\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '-',
            'x\\u00F0', '\\u00A1new!',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'x\\u00f0=\\u00a1new\\!\n',
    ),
    (
        ['set', '--preserve-timestamp', '-', 'e\\u00f0', '\\u00A1new!'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=\\\\u00A1new\\!\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        ['set', '--preserve-timestamp', '-', 'x\\u00F0', '\\u00A1new!'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'x\\\\u00F0=\\\\u00A1new\\!\n',
    ),
    (
        ['set', '--preserve-timestamp', '-', b'e\xC3\xB0', b'\xC2\xA1new!'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=\\u00a1new\\!\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        ['set', '--preserve-timestamp', '-', b'x\xC3\xB0', b'\xC2\xA1new!'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'x\\u00f0=\\u00a1new\\!\n',
    ),
])
def test_cmd_set(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

# --encoding
# --separator
# --outfile
# --preserve-timestamp when there is a timestamp in input
# no --preserve-timestamp, with & without a timestamp in input
# stripping extra trailing line continuations
# universal newlines?
# setting a key that appears multiple times in the file
# reading from a file
# key in source with a non-escaped Latin-1 character
# key with non-BMP character
# setting to a non-BMP character
# setting to a bad surrogate pair?
# invalid \u escape
# setting to the value that the field already has
