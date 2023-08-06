"""
The MIT License (MIT)

Copyright (c) 2015-2021 Kim Blomqvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import sys
import subprocess

from click import ClickException
from .yasha import ENCODING

def do_env(value, default=None):
    return os.environ.get(value, default)

def do_subprocess(cmd, stdout=True, stderr=True, check=True, timeout=2):
    assert sys.version_info >= (3,5)
    kwargs = dict(
        stdout=subprocess.PIPE if stdout else None,
        stderr=subprocess.PIPE if stderr else None,
        shell=True,
        check=False,
        timeout=timeout,
    )

    try:
        result = subprocess.run(cmd, **kwargs)
    except subprocess.TimeoutExpired:
        msg = "Command '{}' timed out after waiting for {} seconds"
        raise ClickException(msg.format(cmd, timeout))

    if check and result.returncode:
        errno = result.returncode
        error = result.stderr.decode().strip()
        msg = "Command '{}' returned non-zero exit status {}\n{}"
        raise ClickException(msg.format(cmd, errno, error))

    return result

def do_shell(cmd, strip=True, check=True, timeout=2):
    result = do_subprocess(cmd, stderr=False, check=check, timeout=timeout)
    if not strip:
        return result.stdout.decode(encoding=ENCODING)
    else:
        return result.stdout.decode(encoding=ENCODING).strip()

FILTERS = {
    'env': do_env,
    'shell': do_shell,
    'subprocess': do_subprocess,
}
