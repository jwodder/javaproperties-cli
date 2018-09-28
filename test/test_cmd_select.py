from   click.testing               import CliRunner
from   javaproperties_cli.__main__ import javaproperties

INPUT = b'''\
foo: bar
key = value
zebra apple
e\\u00f0=escaped
e\\\\u00f0=not escaped
latin-1 = \xF0
bmp = \\u2603
astral = \\uD83D\\uDC10
bad-surrogate = \\uDC10\\uD83D
'''

def test_cmd_select_exists():
    r = CliRunner().invoke(javaproperties, ['select', '-', 'key'], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'#Mon Nov 07 15:29:40 EST 2016\nkey=value\n'

def test_cmd_select_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties select: nonexistent: key not found
'''

def test_cmd_select_some_exist():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'key', 'nonexistent'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
key=value
javaproperties select: nonexistent: key not found
'''

def test_cmd_select_escaped():
    r = CliRunner().invoke(javaproperties, [
        'select', '--escaped', '-', 'e\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\u00f0=escaped
'''

def test_cmd_select_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '--escaped', '-', 'x\\u00F0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties select: x\xC3\xB0: key not found
'''

def test_cmd_select_not_escaped():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'e\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\\\u00f0=not escaped
'''

def test_cmd_select_not_escaped_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'x\\u00f0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties select: x\\u00f0: key not found
'''

def test_cmd_select_utf8():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', b'e\xC3\xB0'  # 'e\u00f0'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
e\\u00f0=escaped
'''

def test_cmd_select_utf8_not_exists():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', b'x\xC3\xB0'
    ], input=INPUT)
    assert r.exit_code == 1
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
javaproperties select: x\xC3\xB0: key not found
'''

def test_cmd_select_latin1_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'latin-1'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
latin-1=\\u00f0
'''

def test_cmd_select_bmp_output():
    r = CliRunner().invoke(javaproperties, ['select', '-', 'bmp'], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
bmp=\\u2603
'''

def test_cmd_select_astral_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'astral'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
astral=\\ud83d\\udc10
'''

def test_cmd_select_bad_surrogate_output():
    r = CliRunner().invoke(javaproperties, [
        'select', '-', 'bad-surrogate'
    ], input=INPUT)
    assert r.exit_code == 0
    assert r.stdout_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
bad-surrogate=\\udc10\\ud83d
'''

# --encoding
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
