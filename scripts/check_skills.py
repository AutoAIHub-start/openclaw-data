"""scripts/check_skills.py - Check all skills for syntax errors"""
import ast
import sys
import pathlib

skills_dir = pathlib.Path("skills")
if not skills_dir.exists():
    print("No skills/ directory found, skipping")
    sys.exit(0)

errors = []
for f in sorted(skills_dir.rglob("*.py")):
    if f.name.startswith("_"):
        continue
    try:
        ast.parse(f.read_text(encoding="utf-8"))
        print(f"  OK: {f}")
    except SyntaxError as e:
        print(f"  ERROR: {f} -> {e}")
        errors.append(f)

print(f"\nPassed: {sum(1 for f in skills_dir.rglob('*.py')) - len(errors)}, Failed: {len(errors)}")
if errors:
    sys.exit(1)
