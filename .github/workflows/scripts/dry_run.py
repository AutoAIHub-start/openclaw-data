"""scripts/dry_run.py - Dry run entry point check"""
import os
import sys
import importlib.util
import pathlib

dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"
if not dry_run:
    print("Not in dry-run mode, skipping")
    sys.exit(0)

print("DRY-RUN mode: loading all skills without making real API calls")

skills_dir = pathlib.Path("skills")
if not skills_dir.exists():
    print("No skills/ directory, skipping")
    sys.exit(0)

errors = []
for f in sorted(skills_dir.rglob("*.py")):
    if f.name.startswith("_"):
        continue
    spec = importlib.util.spec_from_file_location(f.stem, f)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        print(f"  OK: {f}")
    except Exception as e:
        print(f"  FAIL: {f} -> {e}")
        errors.append(f)

print(f"\nLoaded OK: {sum(1 for f in skills_dir.rglob('*.py')) - len(errors)}, Failed: {len(errors)}")
if errors:
    sys.exit(1)

print("All skills loaded successfully!")
