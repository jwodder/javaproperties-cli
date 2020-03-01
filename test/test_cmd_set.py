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
        ['set', '--preserve-timestamp', '-', 'key', 'other value'],
        0,
        b'foo: bar\n'
        b'key=other value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '--unicode', '-',
            'e\\u00F0', '\\u00A1new!',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\xF0=\xA1new\\!\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '--unicode', '-EUTF-8',
            '-', 'e\\u00F0', '\\u00A1new!',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\xC3\xB0=\xC2\xA1new\\!\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
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
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'x\\u00f0=\\u00a1new\\!\n',
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '--unicode',
            '-', 'k\\u00EBy', '\\u94A5',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'k\xEBy=\\u94a5\n'
    ),
    (
        [
            'set', '--preserve-timestamp', '--escaped', '--unicode', '-EUTF-8',
            '-', 'k\\u00EBy', '\\u94A5',
        ],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n'
        b'k\xC3\xABy=\xE9\x92\xA5\n'
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
