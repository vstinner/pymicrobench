import contextlib
import errno
import glob
import os
import subprocess
import sys
import tempfile


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


def test(script, output):
    # write all results into a file to ensure that all test
    # names are unique
    args = [sys.executable, script, "-p1", "-v", "--append", output]
    print("+ " + ' '.join(args))
    proc = subprocess.run(args)
    if proc.returncode:
        sys.exit(proc.returncode)


def run_tests():
    with temporary_file() as tmpfile:
        for script in glob.glob("bench*.py"):
            test(script, tmpfile)


if __name__ == "__main__":
    run_tests()
