Changelog
=========

v0.5.0 (in development)
-----------------------
- Include installation instructions, GitHub links, and changelog in the Read
  the Docs site
- Gave :program:`json2properties` a ``--comment <comment>`` option

v0.4.1 (2018-09-18)
-------------------
- Drop support for Python 2.6 and 3.3
- Support ``javaproperties`` 0.5.0

v0.4.0 (2017-04-22)
-------------------
- Split off the command-line programs from |libpkg|_ into a separate package,
  |clipkg|_

.. |libpkg| replace:: ``javaproperties``
.. _libpkg: https://github.com/jwodder/javaproperties

.. |clipkg| replace:: ``javaproperties-cli``
.. _clipkg: https://github.com/jwodder/javaproperties-cli

v0.3.0 (2017-04-13)
-------------------
- Added the ``PropertiesFile`` class for preserving comments in files [#1]
- The ``ordereddict`` package is now required under Python 2.6

v0.2.1 (2017-03-20)
-------------------
- **Bugfix** to :program:`javaproperties` command: Don't die horribly on
  missing non-ASCII keys
- PyPy now supported

v0.2.0 (2016-11-14)
-------------------
- Added a :program:`javaproperties` command for basic command-line manipulating
  of ``.properties`` files
- Gave :program:`json2properties` a ``--separator`` option
- Gave :program:`json2properties` and :program:`properties2json` ``--encoding``
  options
- Exported the ``java_timestamp()`` function
- ``to_comment()`` now converts CR LF and CR line endings inside comments to LF
- Some minor documentation improvements

v0.1.0 (2016-10-02)
-------------------
Initial release