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
        ['delete', '-', 'key'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '-', 'nonexistent'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n' + INPUT,
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
    (
        ['delete', '--preserve-timestamp', '-', 'key', 'key'],
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
        ['delete', '--preserve-timestamp', '-', 'key', 'bmp'],
        0,
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '--preserve-timestamp', '-', 'bmp', 'key'],
        0,
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'astral = \\uD83D\\uDC10\n',
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

@pytest.mark.parametrize('args,rc,output', [
    (
        ['delete', '--preserve-timestamp', '-', 'key'],
        0,
        b'#Tue Feb 25 19:13:27 EST 2020\n'
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
        b'#Tue Feb 25 19:13:27 EST 2020\n' + INPUT,
    ),
    (
        ['delete', '-', 'key'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'foo: bar\n'
        b'zebra apple\n'
        b'e\\u00f0=escaped\n'
        b'e\\\\u00f0=not escaped\n'
        b'latin-1 = \xF0\n'
        b'bmp = \\u2603\n'
        b'astral = \\uD83D\\uDC10\n',
    ),
    (
        ['delete', '-', 'nonexistent'],
        0,
        b'#Mon Nov 07 15:29:40 EST 2016\n' + INPUT,
    ),
])
def test_cmd_delete_with_timestamp(args, rc, output):
    r = CliRunner().invoke(javaproperties, args,
                           input=b'#Tue Feb 25 19:13:27 EST 2020\n' + INPUT)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_delete_repeated():
    r = CliRunner().invoke(
        javaproperties,
        ['delete', '--preserve-timestamp', '-', 'repeated'],
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
        b'key = value\n'
        b'zebra apple\n'
    )

@pytest.mark.parametrize('args,rc,output', [
    (
        ['delete', '--preserve-timestamp', '-', b'k\xC3\xABy'],
        0,
        b'foo: bar\n'
        b'zebra apple\n',
    ),
    (
        ['delete', '--preserve-timestamp', '--escaped', '-', 'k\\u00EBy'],
        0,
        b'foo: bar\n'
        b'zebra apple\n',
    ),
])
def test_cmd_delete_raw_latin1_key(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=(
        b'foo: bar\n'
        b'k\xEBy = value\n'
        b'zebra apple\n'
    ))
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

@pytest.mark.parametrize('args,rc,output', [
    (
        ['delete', '--preserve-timestamp', '-', b'k\xC3\xABy'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n',
    ),
    (
        ['delete', '--preserve-timestamp', '--escaped', '-', 'k\\u00EBy'],
        0,
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n',
    ),
    (
        [
            'delete', '--preserve-timestamp', '--encoding', 'utf-8',
            '-', b'k\xC3\xABy',
        ],
        0,
        b'foo: bar\n'
        b'zebra apple\n',
    ),
    (
        [
            'delete', '--preserve-timestamp', '-E', 'utf-8', '--escaped',
            '-', 'k\\u00EBy',
        ],
        0,
        b'foo: bar\n'
        b'zebra apple\n',
    ),
])
def test_cmd_delete_raw_utf8_key(args, rc, output):
    r = CliRunner().invoke(javaproperties, args, input=(
        b'foo: bar\n'
        b'k\xC3\xABy = value\n'
        b'zebra apple\n'
    ))
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

@pytest.mark.parametrize('args,rc,output', [
    (
        ['delete', '-T', '-', 'key'],
        0,
        b'foo: bar\n'
        b'zebra apple\n'
    ),
    (
        ['delete', '-T', '-', 'zebra'],
        0,
        b'foo: bar\n'
        b'key = value\n'
    ),
    (
        ['delete', '-T', '-', 'nonexistent'],
        0,
        b'foo: bar\n'
        b'key = value\n'
        b'zebra apple\n'
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
def test_cmd_delete_fix_final_eol(args, rc, inp, output):
    r = CliRunner().invoke(javaproperties, args, input=inp)
    assert r.exit_code == rc, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_delete_header_comments():
    r = CliRunner().invoke(
        javaproperties,
        ['delete', '-', 'key'],
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
        b'zebra apple\n'
    )

# --outfile
# universal newlines?
# reading from a file
# invalid \u escape
