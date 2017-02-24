import contextlib
import errno
import glob
import os
import stat
import subprocess
import sys
import tempfile
import tokenize


SHEBANG = '#!/usr/bin/env python3'


@contextlib.contextmanager
def temporary_file(**kwargs):
    tmp_filename = tempfile.mktemp(**kwargs)
    try:
        yield tmp_filename
    finally:
        try:
            os.unlink(tmp_filename)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise


def check_permission(script):
    st = os.stat(script)
    if not(st.st_mode & stat.S_IXUSR):
        print("ERROR: %s file is not executable" % script)
        sys.exit(1)


def check_shebang(script):
    # check shebang
    with tokenize.open(script) as fp:
        first_line = fp.readline().rstrip()

    if first_line != SHEBANG:
        print("ERROR: %s has no or wrong shebang" % script)
        print("First line: %r" % first_line)
        print("Expected shebang: %r" % SHEBANG)
        sys.exit(1)


def run_script(script, output):
    # --append: write all results into a file to ensure that all test
    # names are unique
    args = [sys.executable, script, "-p1", "-v", "--append", output]
    print("+ " + ' '.join(args))
    proc = subprocess.Popen(args)
    with proc:
        exitcode = proc.wait()
    if exitcode:
        sys.exit(exitcode)


def run_tests():
    with temporary_file() as tmpfile:
        for script in glob.glob("bench*.py"):
            check_permission(script)
            check_shebang(script)
            run_script(script, tmpfile)


if __name__ == "__main__":
    run_tests()
