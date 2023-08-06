pysolbase
============

Welcome to pysol

Copyright (C) 2013/2017 Laurent Labatut / Laurent Champagnac

pysolbase is a set of python helpers to ease development.

It is gevent (co-routines) based.

Usage
===============

Engage gevent monkey patching and setup default logger configuration:

`SolBase.voodoo_init()`

Initialize logging system (without engaging gevent) with default configuration (ie console logs - there is support for syslog and file logs).

`SolBase.logging_init("INFO")`

Re-initialize logging system (without engaging gevent):

`SolBase.logging_init("DEBUG", True)`

Millis helpers:

```
ms = SolBase.mscurrent()
do_something()
ms_elapsed = SolBase.msdiff(ms)
```

Date helpers

```
dt = SolBase.datecurrent()
do_something()
ms_elapsed = SolBase.datediff(dt)
```

Binary helpers

```
bin_buf = SolBase.unicode_to_binary('This is my text buffer', encoding='utf-8')
unicode_string = SolBase.binary_to_unicode(bin_buf, encoding='utf-8')
```

File helpers

```
FileUtility.append_text_to_file('/tmp/test.txt', 'This is my text buffer', 'utf-8')
bin_buf = FileUtility.file_to_binary('/tmp/test.txt')
unicode_string = FileUtility.file_to_text('/tmp/test.txt', 'utf-8')
```

Exception helper

```
try:
   a = None
   b = a + 1
except Exception as e:
   logger.warn("Ex=%s", SolBase.extostr(e))
```


Source code
===============

- We are pep8 compliant (as far as we can, with some exemptions)
- We use a right margin of 360 characters (please don't talk me about 80 chars)
- All unittest files must begin with `test_` or `Test`, should implement setUp and tearDown methods
- All tests must adapt to any running directory
- The whole project is backed by gevent (http://www.gevent.org/)
- We use docstring (:return, :rtype, :param, :type etc), they are mandatory
- We use PyCharm "noinspection", feel free to use them

Requirements
===============

- Debian 10 or greater, x64, Python 3.7

Unittests
===============

To run unittests, you will need:

- nothing special except Python and dependencies requirements.

License
===============

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA


