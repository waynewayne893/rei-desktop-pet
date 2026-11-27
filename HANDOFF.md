# HANDOFF.md｜跨 Agent 统一接续入口

本仓库已完成向 **GitHub-first + Cloud Execution** 迁移、Linux 云端独立恢复验证及 Windows 原生 v2 基础兼容性预验证；原 Windows 本地工作区已正式冻结为历史备份与未来 P5 安装测试环境。

**下一执行器（Antigravity Cloud）请直接阅读并按 [CLOUD_HANDOFF.md](CLOUD_HANDOFF.md) 与 [PROJECT_STATUS.md](PROJECT_STATUS.md) 接续执行。**

---

## 1. 核心基线快照

- **唯一正式私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（`PRIVATE`，`main`）
- **已验证初始资产基线 Commit SHA**：`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（候选标签 `v0.4.0-p4b-candidate`）
- **兼容性预验证分支 Commit SHA**：`6dc14434c1fcaf82ed1a0f996a6a9142b4f5892d`（来自已保留分支 `cloud-bootstrap/p4-compat-preverify`）
- **原生兼容性主控裁定（`REI-P4-COMPAT-MAIN-REVIEW-02`）**：**`BASE_RUNTIME_COMPATIBILITY_PASS`** / **`DETAILED_RUNTIME_VERIFICATION_PARTIAL`**
  - 16 方向逐项映射、`R0C6` 中心死区实际显示行为、完全退出重启持久化与任务事件触发动画留待后续专项验证或 P5 终验，不得标记为已全部通过。
- **当前阶段**：`P4-B_ART_ACCEPTANCE_PASS`。正式 27 动作、171 帧全部人工通过。专项 waiting 六帧及黑服四方向亦通过。 [验收台账](07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json)
- **云端核心环境**：`Ubuntu 24.04.5 LTS` / `Python 3.12.16` / 预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`），无 PyPI 访问（无 NumPy/SciPy），详见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- **图像生成实测边界**：Antigravity 本地 `image-generator` = **`NATIVE_ALPHA_BLOCKED`**
- **主控裁定**：跳过 P4-B-FIX，授权 P4-C。P4-D、P5、P6 仍待授权。

---

## 2. 云端接续顺序

1. 兼容性预验证和基础运行测试已经完成，提交均为专项试验分支的祖先。结项核验记录的远端 `main` 仍在 `0b430a2`。 [合并方案](07_QA验收/P4-B/human-acceptance/CLOSEOUT_AND_MAIN_FF_PLAN.md)
2. 人工原始验收文件已归档。正式 waiting 沿用原版，新版作为通过的备用候选。
3. 统一基准后从独立分支进行 P4-C。先登记黑服已通过的四方向，再生成剩余 44 帧并交人工终审。

---

## 3. 核心交付文档索引

- 云端最终交接手册：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md)
- 云端恢复与环境锁：[CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) · [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- Windows 原生兼容性实测证据：[WINDOWS_COMPAT_TEST_REPORT.md](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_REPORT.md) · [WINDOWS_COMPAT_TEST_RESULT.json](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_RESULT.json) · [WINDOWS_NATIVE_VALIDATION_V2.json](07_QA验收/P4-COMPAT/WINDOWS_NATIVE_VALIDATION_V2.json)
- 云端环境与复算指南：[CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) · [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- 项目实时状态与执行红线：[PROJECT_STATUS.md](PROJECT_STATUS.md) · [AGENTS.md](AGENTS.md)
- P4-B 接管、QA 与矩阵：[AGY_TAKEOVER_REPORT.md](07_QA验收/AGY_TAKEOVER_REPORT.md) · [REI_P4B_QA_REPORT.md](07_QA验收/REI_P4B_QA_REPORT.md) · [REI_P4B_RESUME_MATRIX.json](07_QA验收/REI_P4B_RESUME_MATRIX.json) · [REI_P4B_ASSET_MANIFEST.json](07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- 生图能力边界实测：[AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)
