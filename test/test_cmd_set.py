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
        ['set', '--preserve-timestamp', '-', 'key', 'value'],
        0,
        b'foo: bar\n'
        b'key=value\n'
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
        INPUT + b'nonexistent=mu\n',
    ),
    (
        ['set', '-', 'key', 'other value'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
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
        ['set', '-', 'nonexistent', 'mu'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n' + INPUT + b'nonexistent=mu\n',
    ),
    (
        ['set', '--preserve-timestamp', '-s\t:\t', '-', 'key', 'other value'],
        0,
        b'foo: bar\n'
        b'key\t:\tother value\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xC3\xB0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n'
        b'bad-surrogate = \\uDC10\\uD83D\n',
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

def test_cmd_set_repeated():
    r = CliRunner().invoke(
        javaproperties,
        ['set', '-T', '-', 'repeated', 'nth'],
        input=(
            b'foo: bar\n'
            b'repeated = first\n'
            b'key = value\n'
            b'zebra apple\n'
            b'repeated = second\n'
        ),
    )
    assert r.exit_code == 0, r.stdout_bytes
    assert r.stdout_bytes == (
        b'foo: bar\n'
        b'repeated=nth\n'
        b'key = value\n'
        b'zebra apple\n'
    )

@pytest.mark.parametrize('args,rc,output', [
    (
        ['set', '-T', '-', 'key', 'lock'],
        0,
        b'foo: bar\n'
        b'key=lock\n'
        b'zebra apple\n'
    ),
    (
        ['set', '-T', '-', 'zebra', 'quagga'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra=quagga\n'
    ),
    (
        ['set', '-T', '-', 'nonexistent', 'mu'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'nonexistent=mu\n'
    ),
])
@pytest.mark.parametrize('inp', [
    b'foo: bar\n'
    b'key = value\n'
    b'zebra apple\\\n',

    b'foo: bar\n'
    b'key = value\n'
    b'zebra apple\\',

    b'foo: bar\n'
    b'key = value\n'
    b'zebra apple',
])
def test_cmd_set_fix_final_eol(args, rc, inp, output):
    r = CliRunner().invoke(javaproperties, args, input=inp)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

@pytest.mark.parametrize('args,rc,output', [
    (
        ['set', '--preserve-timestamp', '-', 'key', 'lock'],
        0,
        b'#Tue Feb 25 19:13:27 EST 2020\n'
        b'foo: bar\n'
        b'key=lock\n'
        b'zebra apple\n'
    ),
    (
        ['set', '--preserve-timestamp', '-', 'new', 'shiny!'],
        0,
        b'#Tue Feb 25 19:13:27 EST 2020\n'
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'new=shiny\\!\n'
    ),
    (
        ['set', '-', 'key', 'lock'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo: bar\n'
        b'key=lock\n'
        b'zebra apple\n'
    ),
    (
        ['set', '-', 'new', 'shiny!'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
        b'new=shiny\\!\n'
    ),
])
def test_cmd_set_with_timestamp(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=(
        b'#Tue Feb 25 19:13:27 EST 2020\n'
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
    ))
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

@pytest.mark.parametrize('args,rc,output', [
    (
        ['set', '-T', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\\u00eby=lock\n'
        b'zebra apple\n',
    ),
    (
        ['set', '-T', '--unicode', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\xEBy=lock\n'
        b'zebra apple\n',
    ),
    (
        ['set', '-T', '--escaped', '-', 'k\\u00EBy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\\u00eby=lock\n'
        b'zebra apple\n',
    ),
])
def test_cmd_set_raw_latin1_key(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=(
        b'foo: bar\n'
        b'k\xEBy = value\n'
        b'zebra apple\n'
    ))
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

@pytest.mark.parametrize('args,rc,output', [
    (
        ['set', '-T', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n'
        b'k\\u00eby=lock\n',
    ),
    (
        ['set', '-T', '--unicode', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n'
        b'k\xEBy=lock\n',
    ),
    (
        ['set', '-T', '--escaped', '-', 'k\\u00EBy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n'
        b'k\\u00eby=lock\n',
    ),
    (
        ['set', '-T', '--encoding', 'utf-8', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\\u00eby=lock\n'
        b'zebra apple\n',
    ),
    (
        ['set', '-TU', '--encoding', 'utf-8', '-', b'k\xC3\xABy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy=lock\n'
        b'zebra apple\n',
    ),
    (
        ['set', '-T', '-E', 'utf-8', '--escaped', '-', 'k\\u00EBy', 'lock'],
        0,
        b'foo: bar\n'
        b'k\\u00eby=lock\n'
        b'zebra apple\n',
    ),
])
def test_cmd_set_raw_utf8_key(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=(
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n'
    ))
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_set_header_comments():
    r = CliRunner().invoke(
        javaproperties,
        ['set', '-', 'key', 'lock'],
        input=(
            b'#This is a comment.\n'
            b' ! So is this.\n'
            b'foo: bar\n'
            b'key = value\n'
            b'zebra apple\n'
        ),
    )
    assert r.exit_code == 0, r.stdout_bytes
    assert r.stdout_bytes == (
        b'#This is a comment.\n'
        b' ! So is this.\n'
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo: bar\n'
        b'key=lock\n'
        b'zebra apple\n'
    )

# --outfile
# universal newlines?
# reading from a file
# setting to a non-BMP character
# setting to a bad surrogate pair?
# invalid \u escape
