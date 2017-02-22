import sys

with open(sys.argv[1], 'r+') as f:
    all_lines = list(f)
    all_lines.sort()
    f.seek(0)
    for line in all_lines:
        f.write(line)
