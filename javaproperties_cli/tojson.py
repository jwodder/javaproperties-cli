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

.. option:: -E <encoding>, --encoding <encoding>

    Specifies the encoding of the input file; default value: ``iso-8859-1``
    (a.k.a. Latin-1)
"""

import json
import click
from   javaproperties import load
from   .util          import command, encoding_option, infile_type, outfile_type

@command()
@encoding_option
@click.argument('infile', type=infile_type, default='-')
@click.argument('outfile', type=outfile_type, default='-')
def properties2json(infile, outfile, encoding):
    """Convert a Java .properties file to JSON"""
    with click.open_file(infile, encoding=encoding) as fp:
        props = load(fp)
    with click.open_file(outfile, 'w') as fp:
        json.dump(props, fp, sort_keys=True, indent=4, separators=(',', ': '))
        fp.write('\n')

if __name__ == '__main__':
    properties2json()
