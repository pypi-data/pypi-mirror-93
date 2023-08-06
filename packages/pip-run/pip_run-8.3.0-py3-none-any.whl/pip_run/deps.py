from __future__ import print_function

import os
import sys
import contextlib
import subprocess
import tempfile
import shutil
import itertools
import functools

try:
    from pip._vendor import pkg_resources  # type: ignore
except ImportError:
    import pkg_resources  # type: ignore


def _installable(args):
    """
    Return True only if the args to pip install
    indicate something to install.

    >>> _installable(['inflect'])
    True
    >>> _installable(['-q'])
    False
    >>> _installable(['-q', 'inflect'])
    True
    >>> _installable(['-rfoo.txt'])
    True
    >>> _installable(['projects/inflect'])
    True
    >>> _installable(['~/projects/inflect'])
    True
    """
    return any(
        not arg.startswith('-')
        or arg.startswith('-r')
        or arg.startswith('--requirement')
        for arg in args
    )


@contextlib.contextmanager
def load(*args):
    target = tempfile.mkdtemp(prefix='pip-run-')
    cmd = (sys.executable, '-m', 'pip', 'install', '-t', target) + args
    _installable(args) and subprocess.check_call(cmd)
    try:
        yield target
    finally:
        shutil.rmtree(target)


@contextlib.contextmanager
def _save_file(filename):
    """
    Capture the state of filename and restore it after the context
    exits.
    """
    # For now, only supports a missing filename.
    if os.path.exists(filename):
        tmpl = "Unsupported with extant {filename}"
        raise NotImplementedError(tmpl.format(**locals()))
    try:
        yield
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def pkg_installed(spec):
    try:
        pkg_resources.require(spec)
    except Exception:
        return False
    return True


not_installed = functools.partial(itertools.filterfalse, pkg_installed)
