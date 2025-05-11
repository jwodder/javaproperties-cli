|repostatus| |ci-status| |coverage| |pyversions| |license|

.. |repostatus| image:: https://www.repostatus.org/badges/latest/active.svg
    :target: https://www.repostatus.org/#active
    :alt: Project Status: Active - The project has reached a stable, usable
          state and is being actively developed.

.. |ci-status| image:: https://github.com/jwodder/javaproperties-cli/actions/workflows/test.yml/badge.svg
    :target: https://github.com/jwodder/javaproperties-cli/actions/workflows/test.yml
    :alt: CI Status

.. |coverage| image:: https://codecov.io/gh/jwodder/javaproperties-cli/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/javaproperties-cli

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/javaproperties-cli.svg
    :target: https://pypi.org/project/javaproperties-cli

.. |license| image:: https://img.shields.io/github/license/jwodder/javaproperties-cli.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/javaproperties-cli>`_
| `PyPI <https://pypi.org/project/javaproperties-cli>`_
| `Documentation <https://javaproperties-cli.readthedocs.io>`_
| `Issues <https://github.com/jwodder/javaproperties-cli/issues>`_
| `Changelog <https://github.com/jwodder/javaproperties-cli/blob/master/CHANGELOG.md>`_

``javaproperties-cli`` is a wrapper around the |javaproperties|_ package (from
which it was split off) that provides programs for basic command-line
manipulation of |properties|_ files, including getting, setting, & deleting
values and converting to & from JSON.


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


.. |properties| replace:: ``.properties``
.. _properties: https://en.wikipedia.org/wiki/.properties

.. |javaproperties| replace:: ``javaproperties``
.. _javaproperties: https://github.com/jwodder/javaproperties
