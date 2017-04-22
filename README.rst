.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active - The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.org/jwodder/javaproperties-cli.svg?branch=master
    :target: https://travis-ci.org/jwodder/javaproperties-cli

.. image:: https://coveralls.io/repos/github/jwodder/javaproperties-cli/badge.svg?branch=master
    :target: https://coveralls.io/github/jwodder/javaproperties-cli?branch=master

.. image:: https://img.shields.io/pypi/pyversions/javaproperties-cli.svg
    :target: https://pypi.python.org/pypi/javaproperties-cli

.. image:: https://img.shields.io/github/license/jwodder/javaproperties-cli.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/javaproperties-cli>`_
| `PyPI <https://pypi.python.org/pypi/javaproperties-cli>`_
| `Documentation <https://javaproperties-cli.readthedocs.io/en/v0.4.0>`_
| `Issues <https://github.com/jwodder/javaproperties-cli/issues>`_

``javaproperties-cli`` is a wrapper around the |javaproperties|_ package (from
which it was split off) that provides programs for basic command-line
manipulation of |properties|_ files, including getting, setting, & deleting
values and converting to & from JSON.


Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``javaproperties-cli`` and its dependencies::

    pip install javaproperties-cli

If you happen to be still stuck using Python 2.6, you will need to make sure
that the `ordereddict <https://pypi.python.org/pypi/ordereddict>`_ package is
installed as well: ``pip install ordereddict``


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


.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |javaproperties| replace:: ``javaproperties``
.. _javaproperties: https://github.com/jwodder/javaproperties
