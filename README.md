# pyqt-file-list-widget
PyQt QListWidget for files (Being able to drop the files based on user-defined extensions)

## Requirements
PyQt5 >= 5.8

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-file-list-widget.git --upgrade```

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-show-long-text-as-tooltip-list-widget.git">pyqt-show-long-text-as-tooltip-list-widget</a> - Parent class
* <a href="https://github.com/yjg30737/pyqt-files-already-exists-dialog.git>pyqt-files-already-exists-dialog">pyqt-files-already-exists-dialog</a>

## Method Overview
* `addFilenames(filenames: list, idx=0)` - `idx` is current item index to set. Default is 0.  
* `setFilenames(filenames: list, idx=0)` - Clear the list before adding new files on the list.
* `setFilenameOnly(f: bool)` - Show file name only. ex) C:\...\abc.txt -> abc.txt
* `isFilenameOnly() -> bool`
* `getSelectedFilenames() -> list`
* `removeSelectedRows()`
* `clear()` - Overriding method.
* `getAbsFilename(basename: str) -> str` - Get the absolute file path with base file name.
* `setExtensions(extensions: list)` - Set the acceptable extensions of list.
* `setDuplicateEnabled(f: bool)` - Allow list to have duplicate item.
* `isDuplicateEnabled() -> bool`
* `getFilenameFromRow(r: int) -> str`

## Example
See <a href="https://github.com/yjg30737/pyqt-top-left-right-file-list-widget.git">pyqt-top-left-right-file-list-widget</a>


