.. module:: javaproperties_cli

========================================================================
javaproperties-cli — Command-line manipulation of Java .properties files
========================================================================

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


Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. |properties| replace:: Java ``.properties`` files
.. _properties: https://en.wikipedia.org/wiki/.properties
