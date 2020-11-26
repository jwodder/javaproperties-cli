from   click.testing               import CliRunner
import pytest
from   javaproperties_cli.__main__ import javaproperties

INPUT = (
    b'foo = bar \n'
    b'test \n'
    b' baz = glarch \\\n'
    b'    quux \\\n'
    b'    # comment\n'
    b'xyzzy\n'
    b'\n'
    b'plugh = plo\\\n'
    b'    ver \\\n'
    b'        \\\n'
    b'    stuff \\\n'
    b'\n'
    b'    dwarf\n'
    b'\n'
    b'  \\\n'
    b'   quux\n'
    b'\n'
    b'xyzzy = \xC3\xA9\n'
    b'\n'
    b'  \\\n'
    b'#: after hash\n'
    b'# = bar\n'
    b'\n'
    b'horizontal\\ttab = eight spaces\n'
    b'line\\nfeed = go down one\n'
    b'carriage\\rreturn = go to start of line\n'
    b'goat = \\uD83D\\uDC10\n'
    b'taog = \\uDC10\\uD83D\n'
    b'space = \\ \\ \\ \n'
    b'newline = \\n\n'
    b'latin1 = \\u00e9\n'
    b'\n'
    b'a=b\\\n'
)

OUTPUT = (
    b'#Mon Nov 07 15:29:40 EST 2016\n'
    b'\\#=after hash\n'
    b'a=b\n'
    b'baz=glarch quux \\# comment\n'
    b'carriage\\rreturn=go to start of line\n'
    b'dwarf=\n'
    b'foo=bar \n'
    b'goat=\\ud83d\\udc10\n'
    b'horizontal\\ttab=eight spaces\n'
    b'latin1=\\u00e9\n'
    b'line\\nfeed=go down one\n'
    b'newline=\\n\n'
    b'plugh=plover stuff \n'
    b'quux=\n'
    b'space=\\   \n'
    b'taog=\\udc10\\ud83d\n'
    b'test=\n'
    b'xyzzy=\\u00c3\\u00a9\n'
)

@pytest.mark.parametrize('args,output', [
    (['format'], OUTPUT),
    (['format', '-'], OUTPUT),
    (
        ['format', '-s', ': '],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'\\#: after hash\n'
        b'a: b\n'
        b'baz: glarch quux \\# comment\n'
        b'carriage\\rreturn: go to start of line\n'
        b'dwarf: \n'
        b'foo: bar \n'
        b'goat: \\ud83d\\udc10\n'
        b'horizontal\\ttab: eight spaces\n'
        b'latin1: \\u00e9\n'
        b'line\\nfeed: go down one\n'
        b'newline: \\n\n'
        b'plugh: plover stuff \n'
        b'quux: \n'
        b'space: \\   \n'
        b'taog: \\udc10\\ud83d\n'
        b'test: \n'
        b'xyzzy: \\u00c3\\u00a9\n'
    ),
    (['format', '--ascii'], OUTPUT),
    (
        ['format', '--encoding=UTF-8'],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'\\#=after hash\n'
        b'a=b\n'
        b'baz=glarch quux \\# comment\n'
        b'carriage\\rreturn=go to start of line\n'
        b'dwarf=\n'
        b'foo=bar \n'
        b'goat=\\ud83d\\udc10\n'
        b'horizontal\\ttab=eight spaces\n'
        b'latin1=\\u00e9\n'
        b'line\\nfeed=go down one\n'
        b'newline=\\n\n'
        b'plugh=plover stuff \n'
        b'quux=\n'
        b'space=\\   \n'
        b'taog=\\udc10\\ud83d\n'
        b'test=\n'
        b'xyzzy=\\u00e9\n',
    ),
    (
        ['format', '--unicode'],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'\\#=after hash\n'
        b'a=b\n'
        b'baz=glarch quux \\# comment\n'
        b'carriage\\rreturn=go to start of line\n'
        b'dwarf=\n'
        b'foo=bar \n'
        b'goat=\\ud83d\\udc10\n'
        b'horizontal\\ttab=eight spaces\n'
        b'latin1=\xE9\n'
        b'line\\nfeed=go down one\n'
        b'newline=\\n\n'
        b'plugh=plover stuff \n'
        b'quux=\n'
        b'space=\\   \n'
        b'taog=\\udc10\\ud83d\n'
        b'test=\n'
        b'xyzzy=\xC3\xA9\n',
    ),
    (
        ['format', '--unicode', '--encoding=UTF-8'],
        b'#Mon Nov 07 15:29:40 EST 2016\n'
        b'\\#=after hash\n'
        b'a=b\n'
        b'baz=glarch quux \\# comment\n'
        b'carriage\\rreturn=go to start of line\n'
        b'dwarf=\n'
        b'foo=bar \n'
        b'goat=\xF0\x9F\x90\x90\n'
        b'horizontal\\ttab=eight spaces\n'
        b'latin1=\xC3\xA9\n'
        b'line\\nfeed=go down one\n'
        b'newline=\\n\n'
        b'plugh=plover stuff \n'
        b'quux=\n'
        b'space=\\   \n'
        b'taog=\\udc10\\ud83d\n'
        b'test=\n'
        b'xyzzy=\xC3\xA9\n',
    ),
])
def test_cmd_format(args, output):
    r = CliRunner().invoke(javaproperties, args, input=INPUT)
    assert r.exit_code == 0, r.stdout_bytes
    assert r.stdout_bytes == output

def test_cmd_format_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.properties', 'wb') as fp:
            fp.write(INPUT)
        r = runner.invoke(javaproperties, ['format', 'test.properties'])
        assert r.exit_code == 0
        assert r.stdout_bytes == OUTPUT

# --outfile
# invalid \u escape
