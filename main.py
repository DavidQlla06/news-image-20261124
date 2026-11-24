#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261124.

Runs generate.py (same directory) to draw entry.png, then copies the
result to /output/entry.png, creating /output if needed. Deterministic:
generate.py uses no clock and no randomness, so repeated runs produce
identical bytes.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "generate.py")],
                   check=True)
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")
    print("wrote /output/entry.png")


if __name__ == "__main__":
    main()
