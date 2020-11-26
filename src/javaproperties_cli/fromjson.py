"""
.. program:: json2properties

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

Key ordering is preserved in the output by default (unless the
:option:`--sort-keys` option is given), and numeric, boolean, & null values are
output using their JSON representations; e.g., the input:

.. code-block:: json

    {
        "yes": true,
        "no": "false",
        "nothing": null
    }

becomes:

.. code-block:: properties

    #Mon Sep 26 18:57:44 UTC 2016
    yes=true
    no=false
    nothing=null

.. versionchanged:: 0.7.0
    Key ordering is now preserved by default instead of always being sorted

OPTIONS
^^^^^^^

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

.. option:: -S, --sort-keys

    .. versionadded:: 0.7.0

    Sort entries in output by key

.. option:: -U, --unicode

    .. versionadded:: 0.6.0

    Output non-ASCII characters literally, except for characters that are not
    supported by the output encoding, which are escaped with ``\\uXXXX`` escape
    sequences.  This overrides :option:`--ascii`.
"""

from   collections    import OrderedDict
from   decimal        import Decimal
import json
import click
from   javaproperties import dump
from   .util          import command, encoding_option, outfile_type

@command()
@click.option('-A/-U', '--ascii/--unicode', 'ensure_ascii', default=True,
              help='Whether to escape non-ASCII characters or output raw')
@click.option('-c', '--comment', help='Set comment in output')
@encoding_option
@click.option('-s', '--separator', default='=', show_default=True,
              help='Key-value separator to use in output')
@click.option('-S', '--sort-keys', is_flag=True,
              help='Sort entries in output by key')
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=outfile_type, default='-')
@click.pass_context
def json2properties(ctx, infile, outfile, separator, encoding, comment,
                    ensure_ascii, sort_keys):
    """ Convert a JSON object to a Java .properties file """
    with infile:
        props = json.load(
            infile,
            parse_float=Decimal,
            object_pairs_hook=OrderedDict,
        )
    if not isinstance(props, dict):
        ctx.fail('Only dicts can be converted to .properties')
    strprops = []
    for k,v in props.items():
        assert isinstance(k, str)
        if isinstance(v, (list, dict)):
            ctx.fail('Dictionary values must be scalars, not lists or dicts')
        elif isinstance(v, str):
            strprops.append((k,v))
        elif isinstance(v, Decimal):
            strprops.append((k, str(v)))
        else:
            strprops.append((k, json.dumps(v)))
    with click.open_file(
        outfile, 'w', encoding=encoding, errors='javapropertiesreplace',
    ) as fp:
        dump(strprops, fp, separator=separator, comments=comment,
             ensure_ascii=ensure_ascii, ensure_ascii_comments=ensure_ascii,
             sort_keys=sort_keys)

if __name__ == '__main__':
    json2properties()  # pragma: no cover
