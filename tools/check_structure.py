"""Check repository structure and local imports without executing challenges."""

import ast
import os
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".uv-cache", ".ruff_cache"}


def exported_names(tree: ast.Module) -> set[str]:
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                names.update(item.id for item in ast.walk(target) if isinstance(item, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(item.asname or item.name.split(".")[0] for item in node.names)
    return names


def main() -> int:
    errors = []
    modules = {}
    for directory, children, files in os.walk(ROOT):
        if Path(directory) != ROOT and ".git" in children:
            errors.append(f"Nested Git repository: {Path(directory).relative_to(ROOT)}")
        children[:] = [name for name in children if name not in EXCLUDED]
        for filename in files:
            path = Path(directory) / filename
            relative = path.relative_to(ROOT)
            if filename == "pyproject.toml" and path.parent != ROOT:
                errors.append(f"Redundant project configuration: {relative}")
            if path.suffix == ".py":
                module = ".".join(relative.with_suffix("").parts).removesuffix(".__init__")
                try:
                    modules[module] = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(relative))
                except SyntaxError as exc:
                    errors.append(str(exc))

    exports = {module: exported_names(tree) for module, tree in modules.items()}
    imports_checked = 0
    for module, tree in modules.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                target = node.module
                symbols = [item.name for item in node.names]
            elif isinstance(node, ast.Import):
                for item in node.names:
                    if item.name.startswith(tuple(f"set{i}." for i in range(1, 6))) and item.name not in modules:
                        errors.append(f"{module}: missing module {item.name}")
                continue
            else:
                continue
            if target.split(".")[0] not in {f"set{i}" for i in range(1, 6)}:
                continue
            imports_checked += 1
            if target not in modules:
                errors.append(f"{module}: missing module {target}")
            else:
                for symbol in symbols:
                    if symbol != "*" and symbol not in exports[target]:
                        errors.append(f"{module}: {target} has no symbol {symbol}")

    challenges_checked = 0
    for set_number in range(1, 6):
        directory = ROOT / f"set{set_number}"
        if not (directory / "__init__.py").is_file():
            errors.append(f"{directory.name}: missing __init__.py")
        for challenge in directory.glob("challenge*"):
            if not challenge.is_dir():
                continue
            challenges_checked += 1
            number = challenge.name.removeprefix("challenge")
            if not number.isdigit() or not (set_number - 1) * 8 < int(number) <= set_number * 8:
                errors.append(f"Incorrect challenge number: {challenge.relative_to(ROOT)}")
            if not (challenge / "__init__.py").is_file():
                errors.append(f"{challenge.relative_to(ROOT)}: missing __init__.py")

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    if project["project"]["requires-python"] != lock["requires-python"]:
        errors.append("Python requirement differs between pyproject.toml and uv.lock")
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Structure OK: {challenges_checked} challenges, {len(modules)} Python files, {imports_checked} local imports checked.")
    print("No challenge was imported or executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
