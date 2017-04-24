from   click.testing               import CliRunner
from   freezegun                   import freeze_time
from   javaproperties_cli.fromjson import fromjson

@freeze_time('2016-11-07 20:29:40')
def test_fromjson_empty():
    r = CliRunner().invoke(fromjson, input=b'{}')
    assert r.exit_code == 0
    assert r.output_bytes == b'#Mon Nov 07 15:29:40 EST 2016\n'

@freeze_time('2016-11-07 20:29:40')
def test_fromjson_simple():
    r = CliRunner().invoke(fromjson, input=b'''{
        "key": "value",
        "foo": "bar",
        "zebra": "apple"
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
foo=bar
key=value
zebra=apple
'''

@freeze_time('2016-11-07 20:29:40')
def test_fromjson_truthy():
    r = CliRunner().invoke(fromjson, input=b'''{
        "yes": true,
        "no": false,
        "nothing": null,
        "answer": 42
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
answer=42
no=false
nothing=null
yes=true
'''

@freeze_time('2016-11-07 20:29:40')
def test_fromjson_float():
    r = CliRunner().invoke(fromjson, input=b'''{
        "pi": 3.14159265358979323846264338327950288419716939937510582097494459
    }''')
    assert r.exit_code == 0
    assert r.output_bytes == b'''\
#Mon Nov 07 15:29:40 EST 2016
pi=3.14159265358979323846264338327950288419716939937510582097494459
'''

# arrays
# dicts
# non-dict top level
# non-ASCII characters (escaped & unescaped in input)
# --separator
