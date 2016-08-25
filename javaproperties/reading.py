from   __future__ import unicode_literals
import re
from   six        import StringIO, unichr

def load(fp):
    return dict(load_items(fp))

def loads(s):
    return load(StringIO(s))

def load_items(fp):
    for k,v,_ in load_items3(fp):
        if k is not None:
            yield (k,v)

def load_items3(fp):
    # `fp` must have been opened as Latin-1 (doesn't have to be universal
    # newlines mode) and must support the `readline` method
    # Returns an iterator of `(key, value, source_lines)` tuples; blank lines &
    # comments have `key` & `value` values of `None`
    while True:
        line = source = fp.readline()
        if line == '':
            return
        if re.match(r'^[ \t\f]*(?:[#!]|\r?\n?$)', line):
            yield (None, None, source)
            continue
        line = line.lstrip(' \t\f').rstrip('\r\n')
        while re.search(r'(?<!\\)(?:\\\\)*\\$', line):
            line = line[:-1]
            nextline = fp.readline()  # '' at EOF
            source += nextline
            line += nextline.lstrip(' \t\f').rstrip('\r\n')
        if line == '':  # series of otherwise-blank lines with continuations
            yield (None, None, source)
            continue
        m = re.search(r'(?<!\\)(?:\\\\)*([ \t\f]*[=:]|[ \t\f])[ \t\f]*', line)
        if m:
            yield (unescape(line[:m.start()]), unescape(line[m.end():]), source)
        else:
            yield (unescape(line), '', source)

_unescapes = {'t': '\t', 'n': '\n', 'f': '\f', 'r': '\r'}

def _unesc(m):
    esc = m.group(1)
    if len(esc) == 1:
        return _unescapes.get(esc, esc)
    else:
        return unichr(int(esc[1:], 16))

def _unsurrogate(m):
    c,d = map(ord, m.group())
    return unichr(((c - 0xD800) << 10) + (d - 0xDC00) + 0x10000)

def unescape(field):
    return re.sub(r'[\uD800-\uDBFF][\uDC00-\uDFFF]', _unsurrogate,
                  re.sub(r'\\(u[0-9A-Fa-f]{4}|.)', _unesc, field))
