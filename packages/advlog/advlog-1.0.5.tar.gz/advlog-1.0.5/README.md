# PyAdvancedLogger
Advanced logger inspired by other languages' standard logging classes (e.g. Java and Kotlin).

# Installation
Simply install through `pip install advlog`.

# Example
```python
from advlog import Logger

logger = Logger(logfile='./log.txt')

# Passes varargs on to `print`
# These methods exist: d (debug), v (verbose), i (info), w (warning), e (error), f (fatal)
# Can specify `file` kwarg to write to - next to logfile. d, v, i, w methods default to `sys.stdout`; e, f default to `sys.stderr`.
# Can also specify `None` to only write to `logfile`. One of log file or file keyword must be present.
logger.d('debug', 42)
```

# License
MIT License

Copyright (c) 2020 Kiruse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

