# HQ

[HPI](https://github.com/karlicoss/HPI) got me inspired and I'm trying to play with the idea in smaller scale for myself.

# What is this?
- This is a interface to deal with all the data that I wanna keep. The main functionality is in `hq/views`.

### Notes

#### TIL (27/02/2021):
- appdirs is a lib to help to deal with directories for storing data
- pathlib has nice abstractions to deal with paths on the system, especially checking if they exists or create new ones
- other libs also use the trick to add modules on the path
- method `isatty()` -> True if the file is connected (is associated with a terminal device) to a tty(-like) device (https://gist.github.com/rduplain/e063114479e7470db8d3)
```python
import sys

if sys.stdin.isatty():
    print('you are a tty')
else:
    print('you are not a tty')
```
```bash
$ python isatty.py
you are a tty
$ echo foo | python isatty.py
you are not a tty
$
```

#### TIL (21/03/2021):
- `os.path.expanduser(path)` On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user’s home directory


## Todo
- [ ] Improve `datetime` function to get the time.
- [ ] Define how to deal with images
- [ ] Save articles in multiple files
