import glob
import subprocess
import sys


def test(script):
    args = [sys.executable, script, "-p1", "-v"]
    print("+ " + ' '.join(args))
    proc = subprocess.run(args)
    if proc.returncode:
        sys.exit(proc.returncode)


def run_tests():
    for script in glob.glob("bench*.py"):
        test(script)


if __name__ == "__main__":
    run_tests()
