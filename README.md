# Oxygen Interpreter v0.7
Remake of my Oxygen Interpreter with proper scoping a less bugs.

## How to Use
(assuming you are in repo root)
```
py src/main.py <file_name>
```

For example:

```
py src/main.py tests/test.ox
```

If `py` doesn't work, try `python` or `python3`.

### Options

You can use options to do things. Here are all valid options:

- `-v` or `--version` - Displays interpreter version

## Changelog
v0.7:
- Added arithmetic operators (`+`, `-`, `*`, `/`)

v0.6:
- Added support for multi argument calls
- Added support for multi parameter function definitions
- Added returning

v0.5:
- Added function definitions
- Added interpreter version access (`-v` or `--version`)
- Fully implemented scoping
- Implemented function calls for defined functions

v0.4:
- Added else

v0.3:
- Added if conditions

v0.2:
- Added variables

v0.1:
- Release (printing exists)
