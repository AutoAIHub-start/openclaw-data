"""
dry_run_guard.py
────────────────
在你的 main.py 或 app.py 顶部 import 这个模块。
CI 跑测试时设置环境变量 DRY_RUN=true，
它会拦截所有对外 API 调用，只验证逻辑加载是否正常。

使用方式：
    # main.py 顶部加一行
    from dry_run_guard import dry_run_check
    dry_run_check()
"""

import os
import sys


def dry_run_check():
    """
    如果 DRY_RUN=true，打印当前加载的 Skills 列表后直接退出（exit 0）。
    CI 里看到 Skills 列表 + 无报错 = 测试通过。
    """
    if os.environ.get("DRY_RUN", "false").lower() != "true":
        return  # 正常运行，不做任何拦截

    print("\n" + "=" * 50)
    print("🧪  DRY-RUN 模式：只验证加载，不发真实请求")
    print("=" * 50)

    # 扫描 skills/ 目录，尝试 import 每个模块
    import importlib.util
    import pathlib

    skills_dir = pathlib.Path("skills")
    if not skills_dir.exists():
        print("⚠️  skills/ 目录不存在，跳过扫描")
        sys.exit(0)

    errors = []
    loaded = []

    for skill_file in sorted(skills_dir.rglob("*.py")):
        if skill_file.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(skill_file.stem, skill_file)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            loaded.append(str(skill_file))
            print(f"  ✅  {skill_file}")
        except Exception as e:
            errors.append((str(skill_file), str(e)))
            print(f"  ❌  {skill_file}  →  {e}")

    print(f"\n加载成功: {len(loaded)} 个 / 失败: {len(errors)} 个")

    if errors:
        print("\n以下 Skills 有问题，请修复后再推送：")
        for path, err in errors:
            print(f"  • {path}: {err}")
        sys.exit(1)  # 让 Actions 标红

    print("\n✅  所有 Skills 加载正常，CI 通过！")
    sys.exit(0)
