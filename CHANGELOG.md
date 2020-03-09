v0.6.1 (2020-03-09)
-------------------
- Require `javaproperties` 0.7.\*

v0.6.0 (2020-03-02)
-------------------
- Require `javaproperties` 0.6.\*
- Use `'javapropertiesreplace'` error handler when opening output files
- Gave `javaproperties`' `format`, `select`, and `set` subcommands `--ascii`
  and `--unicode` options for controlling the escaping of non-ASCII characters
  in output
- Gave `properties2json` and `json2properties` `--ascii` and `--unicode`
  options for controlling the escaping of non-ASCII characters in output
- `properties2json` now always outputs UTF-8
- By default, comments output by `json2properties` now have all non-ASCII
  characters escaped rather than all non-Latin-1 characters

v0.5.0 (2020-01-24)
-------------------
- Include installation instructions, GitHub links, and changelog in the Read
  the Docs site
- Gave `json2properties` a `--comment <comment>` option
- Support Python 3.8

v0.4.1 (2018-09-18)
-------------------
- Drop support for Python 2.6 and 3.3
- Support `javaproperties` 0.5.0

v0.4.0 (2017-04-22)
-------------------
- Split off the command-line programs from
  [`javaproperties`](https://github.com/jwodder/javaproperties) into a separate
  package,
  [`javaproperties-cli`](https://github.com/jwodder/javaproperties-cli)

v0.3.0 (2017-04-13)
-------------------
- Added the `PropertiesFile` class for preserving comments in files [#1]
- The `ordereddict` package is now required under Python 2.6

v0.2.1 (2017-03-20)
-------------------
- **Bugfix** to `javaproperties` command: Don't die horribly on missing
  non-ASCII keys
- PyPy now supported

v0.2.0 (2016-11-14)
-------------------
- Added a `javaproperties` command for basic command-line manipulating of
  `.properties` files
- Gave `json2properties` a `--separator` option
- Gave `json2properties` and `properties2json` `--encoding` options
- Exported the `java_timestamp()` function
- `to_comment` now converts CR LF and CR line endings inside comments to LF
- Some minor documentation improvements

v0.1.0 (2016-10-02)
-------------------
Initial release
