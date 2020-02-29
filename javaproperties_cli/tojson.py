# -*- coding: utf-8 -*-
"""
:program:`properties2json`
--------------------------

NAME
^^^^

:program:`properties2json` — Convert a Java ``.properties`` file to JSON

SYNOPSIS
^^^^^^^^

.. code-block:: shell

    properties2json [<OPTIONS>] [<infile> [<outfile>]]

DESCRIPTION
^^^^^^^^^^^

Convert a ``.properties`` file ``infile`` to a JSON object and write the
results to ``outfile``.  If not specified, ``infile`` and ``outfile`` default
to `sys.stdin` and `sys.stdout`, respectively.

OPTIONS
^^^^^^^

.. program:: properties2json

.. option:: -A, --ascii

    Escape all non-ASCII characters in the output with ``\\uXXXX`` escape
    sequences.  This overrides :option:`--unicode`.  This is the default
    behavior.

.. option:: -E <encoding>, --encoding <encoding>

    Specifies the encoding of the input file; default value: ``iso-8859-1``
    (a.k.a. Latin-1)

.. option:: -U, --unicode

    Output non-ASCII characters literally, except for characters that are not
    supported by the output encoding, which are escaped with ``\\uXXXX`` escape
    sequences.  This overrides :option:`--ascii`.
"""

import json
import click
from   javaproperties import load
from   .util          import command, encoding_option, infile_type, outfile_type

@command()
@click.option('-A/-U', '--ascii/--unicode', 'ensure_ascii', default=True,
              help='Whether to escape non-ASCII characters or output raw')
@encoding_option
@click.argument('infile', type=infile_type, default='-')
@click.argument('outfile', type=outfile_type, default='-')
def properties2json(infile, outfile, encoding, ensure_ascii):
    """Convert a Java .properties file to JSON"""
    with click.open_file(infile, encoding=encoding) as fp:
        props = load(fp)
    with click.open_file(outfile, 'w', errors='javapropertiesreplace') as fp:
        json.dump(props, fp, sort_keys=True, indent=4, separators=(',', ': '),
                  ensure_ascii=ensure_ascii)
        fp.write('\n')

if __name__ == '__main__':
    properties2json()
