.. module:: javaproperties_cli

========================================================================
javaproperties-cli — Command-line manipulation of Java .properties files
========================================================================

`GitHub <https://github.com/jwodder/javaproperties-cli>`_
| `PyPI <https://pypi.org/project/javaproperties-cli>`_
| `Documentation <https://javaproperties-cli.readthedocs.io>`_
| `Issues <https://github.com/jwodder/javaproperties-cli/issues>`_
| :doc:`Changelog <changelog>`

`!javaproperties-cli` is a wrapper around the `javaproperties` package (from
which it was split off) that provides programs for basic command-line
manipulation of |properties|_, including getting, setting, & deleting values
and converting to & from JSON.

Currently, the programs only support ``.properties`` files in the simple
line-oriented format, not the XML variant.

.. toctree::
    :caption: Commands
    :maxdepth: 1

    javaproperties
    json2properties
    properties2json
    changelog


Installation
============
``javaproperties-cli`` requires Python 3.10 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``javaproperties-cli`` and its dependencies::

    python3 -m pip install javaproperties-cli


Quickstart
==========

::

    javaproperties get    <file> <key> ...

Output the values of the given keys in the given ``.properties`` file

::

    javaproperties select <file> <key> ...

Output the key-value pairs for the given keys in the given ``.properties`` file

::

    javaproperties set    <file> <key> <value>

Set ``<key>`` in ``<file>`` to ``<value>`` and output the result

::

    javaproperties delete <file> <key> ...

Output the given ``.properties`` file with the given keys deleted

::

    javaproperties format [<file>]

Reformat the given ``.properties`` file, removing comments & extraneous
whitespace and putting keys in sorted order

::

    json2properties [<infile> [<outfile>]]

Convert a JSON object to a ``.properties`` file

::

    properties2json [<infile> [<outfile>]]

Convert a ``.properties`` file to a JSON object


Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: Java ``.properties`` files
.. _properties: https://en.wikipedia.org/wiki/.properties
