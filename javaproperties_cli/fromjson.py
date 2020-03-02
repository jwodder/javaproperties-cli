# -*- coding: utf-8 -*-
"""
:program:`json2properties`
--------------------------

NAME
^^^^

:program:`json2properties` — Convert a JSON object to a Java ``.properties``
file

SYNOPSIS
^^^^^^^^

.. code-block:: shell

    json2properties [<OPTIONS>] [<infile> [<outfile>]]

DESCRIPTION
^^^^^^^^^^^

Convert a JSON file ``infile`` to a ``.properties`` file and write the results
to ``outfile``.  If not specified, ``infile`` and ``outfile`` default to
standard input and standard output, respectively.

The JSON document must be an object with scalar (i.e., string, numeric,
boolean, and/or null) values; anything else will result in an error.

Output is sorted by key, and numeric, boolean, & null values are output using
their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    no=false
    nothing=null
    yes=true

OPTIONS
^^^^^^^

.. program:: json2properties

.. option:: -A, --ascii

    .. versionadded:: 0.6.0

    Escape all non-ASCII characters in the output with ``\\uXXXX`` escape
    sequences.  This overrides :option:`--unicode`.  This is the default
    behavior.

.. option:: -c <comment>, --comment <comment>

    .. versionadded:: 0.5.0

    Show the given string as a comment at the top of the output

.. option:: -E <encoding>, --encoding <encoding>

    Use ``<encoding>`` as the output encoding; default value: ``iso-8859-1``
    (a.k.a. Latin-1)

.. option:: -s <sep>, --separator <sep>

    Use ``<sep>`` as the key-value separator in the output; default value:
    ``=``

.. option:: -U, --unicode

    .. versionadded:: 0.6.0

    Output non-ASCII characters literally, except for characters that are not
    supported by the output encoding, which are escaped with ``\\uXXXX`` escape
    sequences.  This overrides :option:`--ascii`.
"""

from   decimal        import Decimal
import json
import click
from   javaproperties import dump
from   six            import string_types, iteritems
from   .util          import command, encoding_option, outfile_type

@command()
@click.option('-A/-U', '--ascii/--unicode', 'ensure_ascii', default=True,
              help='Whether to escape non-ASCII characters or output raw')
@click.option('-c', '--comment', help='Set comment in output')
@encoding_option
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=outfile_type, default='-')
@click.pass_context
def json2properties(ctx, infile, outfile, separator, encoding, comment,
                    ensure_ascii):
    """Convert a JSON object to a Java .properties file"""
    with infile:
        props = json.load(infile, parse_float=Decimal)
    if not isinstance(props, dict):
        ctx.fail('Only dicts can be converted to .properties')
    strprops = []
    for k,v in iteritems(props):
        assert isinstance(k, string_types)
        if isinstance(v, (list, dict)):
            ctx.fail('Dictionary values must be scalars, not lists or dicts')
        elif isinstance(v, string_types):
            strprops.append((k,v))
        elif isinstance(v, Decimal):
            strprops.append((k, str(v)))
        else:
            strprops.append((k, json.dumps(v)))
    strprops.sort()
    with click.open_file(
        outfile, 'w', encoding=encoding, errors='javapropertiesreplace',
    ) as fp:
        dump(strprops, fp, separator=separator, comments=comment,
             ensure_ascii=ensure_ascii, ensure_ascii_comments=ensure_ascii)

if __name__ == '__main__':
    json2properties()
