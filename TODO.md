- Write tests
    - Handle the fact that `stdout_bytes` will contain CR LF line endings (I
      think) on Windows
    - Test the programs' nontrivial components (e.g., `setproperties`) in
      isolation?
    - Test on Windows with Appveyor?
- Add docstrings for the private functions
- Add a test environment that installs the latest development version of
  `javaproperties`
- (Re)document how the commands can be invoked with Python's `-m` option
- Show a more human-friendly error message (At the very least, omit the
  traceback) on an `InvalidUEscapeError`
- Rename the `javaproperties` command to something shorter?
- Rename the `javaproperties_cli` module to something shorter?

- `javaproperties` command:
    - Give `set`, `delete`, and `format` (and `select`?) `--in-place` options
      (with optional `--backup <file>`) as an alternative to `--outfile`
        - `--backup` implies `--in-place`
    - Give `set` and `delete` a `--format` option for also reformatting
        - `set`: When `--format` is given, `--ascii` and `--unicode` affect all
          entries
        - `delete`: Add `--ascii` and `--unicode` options for controlling what
          characters to escape when reformatting
            - Passing `-A`/-U` to `delete` without `--format` is either an
              error or a no-op
    - Give `format` and `select` `--preserve-timestamp` options
    - Add options for completely suppressing the timestamp
    - Give `select` an option for preserving formatting? (Preserve by default?)
    - Give `format` (and `set`? `select`? `delete`?) an option for setting the
      comment in the output
    - Give `format` an option for preserving the header comment/all comments ?
    - `set` and `delete`: Update the timestamp only if an actual change is
      made?
        - This will require eliminating the whole "streaming editing" thing and
          just using `PropertiesFile` instead (which might be a good idea
          regardless)
    - `set`: Add options for whether to replace the first or last occurrence of
      the key?
    - Give `format` an option for using a different output encoding than input
      encoding?
    - `set` and `delete`: Don't automatically strip trailing line continuations
      from the last line of the file?
    - Support "chaining" subcommands so that one can write, say,
      "`javaproperties infile.properties set foo bar set key value delete zebra
      format`" ?

- Support XML properties files:
    - Add `javaproperties fromxml` and `javaproperties toxml` commands for
      converting between XML format and simple line-oriented format
        - Be sure to preserve (leading) comments!
    - `javaproperties {get,set,select,delete,format}`: support XML properties
      files
        - Autodetect whether a properties file is XML based on file extension?
        - Add an option for forcing arguments to be treated as XML files?
    - Support converting between JSON and XML properties

- Add a `javaproperties merge` command for merging two (or more?) properties
  files (or, equivalently, updating one properties file based on another)
    - Note that just concatenating the two files (optionally followed by
      reformatting to eliminate duplicates) will not work 100% of the time due
      to the possibility of the first file ending with a line continuation
- Make `json2properties` and `properties2json` into subcommands of
  `javaproperties` named `fromjson` and `tojson`?
- Give `propertes2json` options for preserving the comment & timestamp in
  `__comment__` and `__timestamp__` keys?
- `json2properties`: Better handle input encoding
    - `json.load()` only started accepting bytes in Python 3.6
- `json2properties`: Add an option for suppressing the timestamp
