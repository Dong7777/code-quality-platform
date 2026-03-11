import os
import re
import sys

errors = []

func_pattern = re.compile(r'^\s*[A-Za-z_][\w\s\*]*\s+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{')
global_var_pattern = re.compile(
    r'^\s*(?!static\b)(?:extern\s+)?(?:unsigned|signed|const|volatile|int|char|short|long|float|double|uint\d+_t|int\d+_t|bool|struct\s+\w+)\s+([A-Za-z_]\w*)\s*(=.*)?;'
)
static_var_pattern = re.compile(
    r'^\s*static\s+(?:unsigned|signed|const|volatile|int|char|short|long|float|double|uint\d+_t|int\d+_t|bool|struct\s+\w+)\s+([A-Za-z_]\w*)\s*(=.*)?;'
)
struct_typedef_pattern = re.compile(r'^\s*typedef\s+struct\b.*\b([A-Za-z_]\w*)\s*;')
enum_typedef_pattern = re.compile(r'^\s*typedef\s+enum\b.*\b([A-Za-z_]\w*)\s*;')
macro_pattern = re.compile(r'^\s*#\s*define\s+([A-Za-z_]\w*)')

def is_snake_case(name: str) -> bool:
    return re.fullmatch(r'[a-z][a-z0-9_]*', name) is not None

def is_upper_snake(name: str) -> bool:
    return re.fullmatch(r'[A-Z][A-Z0-9_]*', name) is not None

def check_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for lineno, line in enumerate(f, 1):
            m = func_pattern.match(line)
            if m:
                name = m.group(1)
                if not is_snake_case(name):
                    errors.append(f'{path}:{lineno}: 函数名应为小写下划线: {name}')

            m = global_var_pattern.match(line)
            if m:
                name = m.group(1)
                if not name.startswith('g_'):
                    errors.append(f'{path}:{lineno}: 全局变量应使用 g_ 前缀: {name}')

            m = static_var_pattern.match(line)
            if m:
                name = m.group(1)
                if not name.startswith('s_'):
                    errors.append(f'{path}:{lineno}: 静态变量应使用 s_ 前缀: {name}')

            m = struct_typedef_pattern.match(line)
            if m:
                name = m.group(1)
                if not name.startswith('T_'):
                    errors.append(f'{path}:{lineno}: 结构体类型应使用 T_ 前缀: {name}')

            m = enum_typedef_pattern.match(line)
            if m:
                name = m.group(1)
                if not name.startswith('E_'):
                    errors.append(f'{path}:{lineno}: 枚举类型应使用 E_ 前缀: {name}')

            m = macro_pattern.match(line)
            if m:
                name = m.group(1)
                if not is_upper_snake(name):
                    errors.append(f'{path}:{lineno}: 宏名应全大写下划线: {name}')

def main() -> None:
    for root, _, files in os.walk('.'):
        if '.git' in root or '.github' in root:
            continue
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):
                check_file(os.path.join(root, file))

    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    print('命名检查通过')

if __name__ == '__main__':
    main()