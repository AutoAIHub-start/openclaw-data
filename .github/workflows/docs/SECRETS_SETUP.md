# 🔐 GitHub Secrets 配置指南

本文件说明在私有仓库中需要配置哪些 Secrets，供 CI/CD 和 OpenClaw 运行时使用。

---

## 第一步：进入 Secrets 设置页

```
你的仓库 → Settings → Secrets and variables → Actions → New repository secret
```

---

## 需要添加的 Secrets 清单

| Secret 名称         | 填写内容                              | 用途                          |
|---------------------|---------------------------------------|-------------------------------|
| `HF_TOKEN`          | Hugging Face Access Token             | Actions 部署/同步 HF Space    |
| `OPENAI_API_KEY`    | OpenAI 或你用的 LLM API Key           | dry-run 时跳过，正式运行时用  |
| `GITHUB_PAT`        | GitHub Personal Access Token          | Issue 读写脚本使用            |
| `PUSHEER_KEY`       | Server酱/PushDeer 的推送 Key          | 测试失败时发手机通知（可选）  |

> ⚠️ **绝对不要**把任何 Key 硬编码在代码里，Private 仓库也一样。

---

## 第二步：在代码里读取

```python
import os

HF_TOKEN      = os.environ.get("HF_TOKEN", "")
OPENAI_KEY    = os.environ.get("OPENAI_API_KEY", "")
DRY_RUN       = os.environ.get("DRY_RUN", "false").lower() == "true"

if DRY_RUN:
    print("[dry-run] 跳过真实 API 调用，只验证逻辑加载")
    # 不发请求，只做结构检查
```

---

## 第三步（可选）：区分 Production / Development 环境

```
Settings → Environments → New environment
```

创建两个环境：
- `development`：填测试 Key，无需审批
- `production`  ：填正式 Key，可设置"需要手动审批才能部署"

在 Workflow 里指定环境：

```yaml
jobs:
  deploy:
    environment: production   # 或 development
    steps:
      ...
```

这样本地/测试用测试 Key，推到 main 分支才用正式 Key，互不污染。
