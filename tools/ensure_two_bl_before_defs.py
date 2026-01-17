#!/usr/bin/env python3
import os
root = r'C:\Users\andre\source\repos\gmr'
count = 0
targets = ['gmr', 'tests']
for t in targets:
    base = os.path.join(root, t)
    if not os.path.isdir(base):
        continue
    for dirpath, dirs, files in os.walk(base):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(dirpath, f)
                with open(path, 'r', encoding='utf-8') as fh:
                    lines = fh.readlines()
                changed = False
                i = 0
                out_lines = []
                while i < len(lines):
                    line = lines[i]
                    if line.startswith('def ') or line.startswith('class '):
                        # count previous consecutive blank lines
                        prev_blank = 0
                        j = len(out_lines) - 1
                        while j >= 0 and out_lines[j].strip() == '':
                            prev_blank += 1
                            j -= 1
                        needed = 2 - prev_blank
                        if needed > 0:
                            out_lines.extend(['\n'] * needed)
                            changed = True
                    out_lines.append(line)
                    i += 1
                if changed:
                    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                        fh.writelines(out_lines)
                    count += 1
print(f'Adjusted {count} files')
