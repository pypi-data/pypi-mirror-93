# sg.py -- a small static site generator

## Installation

```bash
$ pip install sg.py
```


## Usage

Populate directory with markdown files (they have to end with
.markdown). You can also create arbitrarily nested subdirectories
containing .markdown files.

Sg will go recursively through all directories not beginning with an
underscore ("_") and convert the .markdown files into .html. The
resulting HTML files will be saved into the _site directory, conserving
the directory structure where the .markdown file was found.

Put your static content into _static. Files and subdirectories will be
copied into _site without any modifications.

## TODO

* document the YAML frontmatter
* enable layout selection by _layout_foo or so
