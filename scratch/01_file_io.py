"""Day 1, script 1 of 5 — file I/O and context managers.

TASK
  Read scratch/sample.txt inside a `with open(...)` block.
  Count the non-empty lines.
  Write a one-line summary to scratch/summary.txt.

WHAT TO NOTICE
  `with` closes the file even if the body raises. There is no PHP equivalent;
  it replaces the try/finally you would write by hand.

DONE WHEN
  `uv run python scratch/01_file_io.py` prints the count and summary.txt exists.
"""

# TODO: your code here

with open("scratch/sample.txt", "r") as f:
    lines = f.readlines()
    non_empty_lines = [line for line in lines if line.strip()]
    count = len(non_empty_lines)

with open("scratch/summary.txt", "w") as f:
    f.write(f"Non-empty lines: {count}")
    print(f"Non-empty lines: {count}")