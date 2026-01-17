#!/usr/bin/env python3
import os
root = r'C:\Users\andre\source\repos\gmr'
count = 0
for dirpath, dirs, files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            # Replace runs of 3 or more newlines with two newlines
            new_content = content
            while '\n\n\n' in new_content:
                new_content = new_content.replace('\n\n\n', '\n\n')
            if new_content != content:
                with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(new_content)
                count += 1
print(f'Collapsed blank lines in {count} files')
