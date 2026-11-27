# HANDOFF.md｜跨 Agent 统一接续入口

本仓库已完成向 **GitHub-first + Cloud Execution** 迁移，原 Windows 本地工作区已正式冻结为历史备份与未来 P5 安装测试环境。

**下一执行器（Antigravity Cloud）请直接阅读并按 [CLOUD_HANDOFF.md](CLOUD_HANDOFF.md) 接续执行。**

---

## 1. 核心基线快照

- **唯一正式私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（`PRIVATE`，`main`）
- **已验证远程资产基线 Commit SHA**：`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（候选标签 `v0.4.0-p4b-candidate`）
- **当前真实阶段**：`P4-B PARTIAL`（171 帧候选齐备、结构与离线 QA 通过、人工美术验收尚未全部完成；非 `v1.0.0`）
- **图像生成实测边界**：Antigravity 本地 `image-generator` = **`NATIVE_ALPHA_BLOCKED`**
- **未授权阶段**：`P4-C`、`P4-D`、`P5`、`P6` 均未授权，严禁提前启动

---

## 2. 云端接续顺序

1. 在 Antigravity Cloud（Linux）克隆仓库并安装 [requirements.txt](requirements.txt)；
2. 执行 Linux 云端独立恢复验证：
   ```bash
   python3 06_共用工具/rei_atlas_tools.py verify
   python3 06_共用工具/rei_atlas_tools.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets
   ```
3. 按主控后续授权依次进入：`REI-PET-REVIEW-CENTER-V1.0` → `REI-PET-P4-B-FIX`（待主控裁定透明度方案与修复清单）→ 后续各阶段。

---

## 3. 核心交付文档索引

- 云端最终交接手册：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md)
- 云端迁移最终报告：[GIT_CLOUD_MIGRATION_FINAL_REPORT.md](GIT_CLOUD_MIGRATION_FINAL_REPORT.md)
- 云端环境与复算指南：[CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) · [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- 项目实时状态与执行红线：[PROJECT_STATUS.md](PROJECT_STATUS.md) · [AGENTS.md](AGENTS.md)
- P4-B 接管、QA 与矩阵：[AGY_TAKEOVER_REPORT.md](07_QA验收/AGY_TAKEOVER_REPORT.md) · [REI_P4B_QA_REPORT.md](07_QA验收/REI_P4B_QA_REPORT.md) · [REI_P4B_RESUME_MATRIX.json](07_QA验收/REI_P4B_RESUME_MATRIX.json) · [REI_P4B_ASSET_MANIFEST.json](07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- 生图能力边界实测：[AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)
