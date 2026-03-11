import os
import re
import sys

errors = []

header_guard_ifndef = re.compile(r'^\s*#ifndef\s+([A-Z0-9_]+)\s*$')
header_guard_define = re.compile(r'^\s*#define\s+([A-Z0-9_]+)\s*$')

def check_header_guard(path: str) -> None:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if len(lines) < 3:
        errors.append(f'{path}: 头文件过短，缺少保护宏')
        return

    guard1 = None
    guard2 = None
    for line in lines[:5]:
        m = header_guard_ifndef.match(line)
        if m:
            guard1 = m.group(1)
            break

    for line in lines[:8]:
        m = header_guard_define.match(line)
        if m:
            guard2 = m.group(1)
            break

    if not guard1 or not guard2 or guard1 != guard2:
        errors.append(f'{path}: 头文件保护宏不完整或不匹配')

def check_c_has_header(path: str) -> None:
    base, _ = os.path.splitext(path)
    header = base + '.h'
    if not os.path.exists(header):
        errors.append(f'{path}: 缺少同名头文件 {os.path.basename(header)}')

def main() -> None:
    for root, _, files in os.walk('.'):
        if '.git' in root or '.github' in root:
            continue
        for file in files:
            full = os.path.join(root, file)
            if file.endswith('.h'):
                check_header_guard(full)
            elif file.endswith('.c'):
                check_c_has_header(full)

    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    print('头文件检查通过')

if __name__ == '__main__':
    main()