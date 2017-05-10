- Write tests
    - Handle the fact that `output_bytes` will contain CR LF line endings (I
      think) on Windows
    - Test the programs' nontrivial components (e.g., `setproperties`) in
      isolation?
    - Test `properties2json` and `json2properties`
    - Test on Windows with Appveyor?
- Add docstrings for the private functions
- Restrict `TIMESTAMP_RGX` to only match C locale timestamps?
- Restrict `TIMESTAMP_RGX` to only consider `[ \t\f]` as whitespace?

- `javaproperties` command:
    - Give `set`, `delete`, and `format` (and `select`?) `--in-place` options
      (with optional `--backup <file>`) as an alternative to `--outfile`
        - `--backup` implies `--in-place`
    - Give `set` and `delete` a `--format` option for also reformatting
    - Give `format` and `select` `--preserve-timestamp` options
    - Add options for completely suppressing the timestamp
    - Give `select` an option for preserving formatting? (Preserve by default?)
    - `select`: Don't output a timestamp if none of the given keys are defined?
    - Give `get` an option for escaping output values?
    - Give `format` an option for setting the comment in the output?
    - `set` and `delete`: Try to only modify the timestamp if an actual change
      is made

- Support XML properties files:
    - Support converting between JSON and XML properties
    - Add a command for converting between XML format and simple line-oriented
      format
    - Support autodetecting whether a properties file is in XML based on file
      extension (or other means?) ?
    - Support by just adding `properties2xml` and `xml2properties` commands?

- Add a command for merging two (or more?) properties files (or, equivalently,
  updating one properties file based on another)
- Give `properties2json` and `json2properties` options for preserving the order
  of the input keys
- Give `json2properties` an option for setting the comment?
