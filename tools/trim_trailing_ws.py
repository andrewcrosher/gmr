#!/usr/bin/env python3
import os
root = r'C:\Users\andre\source\repos\gmr'
count = 0
for dirpath, dirs, files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()
            new_lines = []
            changed = False
            for line in lines:
                if line.strip() == '':
                    if line != '\n':
                        changed = True
                    new_lines.append('\n')
                else:
                    new_line = line.rstrip() + '\n'
                    if new_line != line:
                        changed = True
                    new_lines.append(new_line)
            if changed:
                with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.writelines(new_lines)
                count += 1
print(f'Cleaned {count} files')
