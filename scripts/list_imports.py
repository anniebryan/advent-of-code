#!/usr/bin/env python3

import ast
from collections import Counter
from pathlib import Path

PROJECT_DIRS = [f"aoc_{year}" for year in range(2018, 2026)]

def find_python_files(root: Path):
    for subdir in PROJECT_DIRS:
        subpath = root / subdir
        if subpath.exists():
            for path in subpath.rglob("*.py"):
                yield path


def extract_imports_from_file(path: Path):
    imports = []

    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")

    return imports


def main():
    project_root = Path(__file__).resolve().parent.parent
    import_counter = Counter()

    for py_file in find_python_files(project_root):
        file_imports = extract_imports_from_file(py_file)
        import_counter.update(file_imports)

    print("=== All imports sorted by frequency ===")
    for imp, count in import_counter.most_common():
        print(f"{count:3}  {imp}")

    print("\n=== Unique imports (alphabetical) ===")
    for imp in sorted(import_counter):
        print(imp)


if __name__ == "__main__":
    main()
