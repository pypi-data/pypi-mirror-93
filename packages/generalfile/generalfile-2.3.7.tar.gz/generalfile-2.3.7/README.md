# generalfile 2.3.7
Easily manage files cross platform.

[![workflow Actions Status](https://github.com/ManderaGeneral/generalfile/workflows/workflow/badge.svg)](https://github.com/ManderaGeneral/generalfile/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/ManderaGeneral/generalfile)
[![PyPI version shields.io](https://img.shields.io/pypi/v/generalfile.svg)](https://pypi.org/project/generalfile/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/generalfile.svg)](https://pypi.python.org/pypi/generalfile/)
[![Generic badge](https://img.shields.io/badge/platforms-windows%20%7C%20ubuntu-blue.svg)](https://shields.io/)

## Contents
<pre>
<a href='#generalfile-2.3.7'>generalfile 2.3.7</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                                | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/send2trash'>send2trash</a>   | <a href='https://pypi.org/project/appdirs'>appdirs</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   |
|:---------------------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|
| `pip install generalfile`              | Yes                                                                    | Yes                                                            | Yes                                                      | No                                                     |
| `pip install generalfile[spreadsheet]` | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |
| `pip install generalfile[full]`        | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/__init__.py#L1'>Module: generalfile</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/errors.py#L4'>Class: CaseSensitivityError</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/errors.py#L5'>Class: InvalidCharacterError</a>
└─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L58'>Method: absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_lock.py#L124'>Method: as_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: copy</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L211'>Method: copy_to_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L321'>Method: create_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L35'>Method: delete</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L35'>Method: delete_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L101'>Method: endswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L239'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L31'>Method: get_alternative_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L338'>Method: get_cache_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: get_differing_files</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L346'>Method: get_lock_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L41'>Method: get_lock_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path.py#L41'>Method: get_parent</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L47'>Method: get_path_from_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: get_paths_in_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: get_paths_recursive</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L21'>Method: get_replaced_alternative_characters</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L354'>Method: get_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L81'>Method: is_absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L227'>Method: is_file</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L233'>Method: is_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L452'>Method: is_identical</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L87'>Method: is_relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_lock.py#L115'>Method: lock</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L251'>Method: match</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L219'>Method: move</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L156'>Method: name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L331'>Method: open_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L94'>Method: open_operation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L149'>Method: parts</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L120'>Method: read</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L69'>Method: relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L125'>Method: remove_end</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L109'>Method: remove_start</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: rename</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L141'>Method: same_destination</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: seconds_since_creation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: seconds_since_modified</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L374'>Method: set_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L11'>Method: size</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L93'>Method: startswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L170'>Method: stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L198'>Method: suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L237'>Method: suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L35'>Method: trash</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L35'>Method: trash_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L184'>Method: true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path.py#L117'>Method: view</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L162'>Method: with_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L176'>Method: with_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L204'>Method: with_suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L243'>Method: with_suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_strings.py#L190'>Method: with_true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L259'>Method: without_file</a>
   └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/ce46082/generalfile/path_operations.py#L108'>Method: write</a>
</pre>

## Todo
| Module              | Message                                                                                     |
|:--------------------|:--------------------------------------------------------------------------------------------|
| path\_lock.py        | other\_paths                                                                                 |
| decorators.py       | Put this in library                                                                         |
| path.py             | Add a proper place for all variables, add working\_dir, sys.executable and sys.prefix to it. |
| path.py             | Raise suppressable warning if space in Path.                                                |
| path\_operations.py  | Can we not just change signature to rename(self, new\_path, overwrite=False) ?               |
| path\_operations.py  | Filter for Path.get\_paths\_* like we have in ObjInfo.                                        |
| path\_operations.py  | Add this error parameter for more methods                                                   |
| path\_operations.py  | Tests for get\_differing\_files.                                                              |
| path\_spreadsheet.py | Make it order columns if there are any so that they line up with append.                    |
| path\_spreadsheet.py | Should probably support DataFrame and Series as well.                                       |

<sup>
Generated 2021-02-04 12:34 CET for commit <a href='https://github.com/ManderaGeneral/generalfile/commit/ce46082'>ce46082</a>.
</sup>
