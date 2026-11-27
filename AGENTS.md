# AGENTS.md｜Rei Desktop Pet 跨 Agent 工程执行规则（GitHub-first + Cloud Execution）

本文件为所有接入本仓库的执行器（Antigravity Cloud、Antigravity Local 及后续授权 Agent）的最高优先级执行约束。

---

## 1. 数据源与角色分工

- **唯一正式数据源**：GitHub 私有仓库 `https://github.com/waynewayne893/rei-desktop-pet.git`（`Private`，默认分支 `main`）。
- **执行模式**：优先在 **Antigravity Cloud** 接入本仓库执行后续开发；原 Windows 本地工作区保留为历史备份及最终 P5 桌面安装测试环境。
- **治理分工**：ChatGPT 为项目主控（阶段裁定与授权）；Antigravity 为工程执行器（已正式接替 Codex）；用户负责人工美术终审。
- **铁律**：**禁止将文件存在、目录存在、Git Push 成功或脚本 `PASS` 等同于人工美术验收通过，也禁止将候选版本标记为正式 `v1.0.0`。**

---

## 2. 强制保护与禁止事项

1. **严禁修改冻结资产**：`00_原始美术母版/`（含 `P2_字节备份/`）与 `02_标准化母版/` 已冻结派生母版（含 `P3-FIX` 白服修复版）只读不可改；不得为了跨平台迁移修改任何已冻结原图或已验收帧字节。
2. **严禁覆盖历史记录与拒收件**：保留全部 Codex 历史报告、清单、拒收原图（白服 `P4-A/originals/idle/attempt-01`、黑服旧 `running-right`）及 Antigravity 接管与能力测试留档。旧黑服 `running-right` 严禁进入图集；新版黑服 `running-right`（`FIX-BLACK`）已人工验收，禁止重做。
3. **严禁擅自拷贝受限组件**：不得复制或分发 Windows `OpenAI.Codex` MSIX 内置 `hatch-pet` 脚本至本仓库。云端校验与图集重装统一使用本仓库洁净跨平台工具 [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py)。
4. **严禁破坏性或越权操作**：
   - 禁止删除原有本地工程、禁止修改明日香工程及已有安装宠物；
   - 禁止公开仓库、禁止上传账号凭据、禁止强制 Push (`--force`)；
   - 禁止在未获主控授权时提前进入 P4-C、P4-D、P5、P6；
   - 禁止开发形态热切换、禁止修改 Codex 应用本体、禁止用 Python 仿射变形冒充真实生成人物动作。

---

## 3. 跨平台与图像生成边界

- **跨平台编码要求**：所有新增工程脚本必须使用 `pathlib` + 仓库相对路径 + 可配置 `--root`，严禁硬编码 Windows 盘符或 `C:/Windows/Fonts/*`。
- **图像生成实测边界**：Antigravity `image-generator` 经实测为 `NATIVE_ALPHA_BLOCKED`（角色还原极高，但仅输出不透明 RGB JPEG、最大 `16:9`），证据见 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)。获主控裁定替代管线前，禁止私自对不透明生图去背冒充原生透明条带。

---

## 4. 新会话接入必读顺序

1. [PROJECT_STATUS.md](PROJECT_STATUS.md)
2. [HANDOFF.md](HANDOFF.md)
3. [CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) & [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
4. [07_QA验收/REI_P4B_RESUME_MATRIX.json](07_QA验收/REI_P4B_RESUME_MATRIX.json)
