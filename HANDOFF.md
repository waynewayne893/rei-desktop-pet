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
- **当前阶段**：`P4-C_ART_ACCEPTANCE_PASS` / `P4-D_FINAL_ASSEMBLY_AUTHORIZED`。正式 27 动作 171 帧与 3 形态 48 方向帧（合计 219 帧）全部完成人工验收绑定。[P4-B 验收台账](07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json) · [P4-C 验收台账](07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json)
- **云端核心环境**：`Ubuntu 24.04.5 LTS` / `Python 3.12.16` / 预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`），无 PyPI 访问（无 NumPy/SciPy），详见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- **图像生成实测边界**：Antigravity 本地 `image-generator` = **`NATIVE_ALPHA_BLOCKED`**（全部美术生产已结束，P4-D 阶段无需调用生图）
- **主控裁定**：`P4-B-FIX_SKIPPED`、`P4-C_ART_ACCEPTANCE_PASS`、`P4-D_FINAL_ASSEMBLY_AUTHORIZED`。P5、P6 仍待授权。

---

## 2. 接续顺序

1. 核验时远端 `main` 指向 `6b4229f`、`feat/p4c-production` 指向 `be86cce`。取得用户明确授权后，按 [P4-C 结项与 main 统一方案](07_QA验收/P4-C/human-acceptance/P4C_CLOSEOUT_AND_MAIN_FF_PLAN.md) 将 P4-C 结项提交 fast-forward 推进至 `main`。
2. 从统一后的 `main` 切出独立任务分支 `feat/p4d-final-assembly`，基于 Python 标准库 + Pillow 工具链装配校服、白服 00、黑服 09 三套 `1536×2288` v2 扩展图集、执行 264 格全量离线 QA 与打包交付，并编写 Windows P5 运行验收指南。
3. 严禁在未获授权前执行 Windows 安装或正式发布；完成后由 ChatGPT 主控独立验收 P4-D。

---

## 3. 核心交付文档索引

- 云端最终交接手册：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md)
- 云端恢复与环境锁：[CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) · [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- Windows 原生兼容性实测证据：[WINDOWS_COMPAT_TEST_REPORT.md](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_REPORT.md) · [WINDOWS_COMPAT_TEST_RESULT.json](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_RESULT.json) · [WINDOWS_NATIVE_VALIDATION_V2.json](07_QA验收/P4-COMPAT/WINDOWS_NATIVE_VALIDATION_V2.json)
- 云端环境与复算指南：[CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) · [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- 项目实时状态与执行红线：[PROJECT_STATUS.md](PROJECT_STATUS.md) · [AGENTS.md](AGENTS.md)
- P4-B 接管、QA 与矩阵：[AGY_TAKEOVER_REPORT.md](07_QA验收/AGY_TAKEOVER_REPORT.md) · [REI_P4B_QA_REPORT.md](07_QA验收/REI_P4B_QA_REPORT.md) · [REI_P4B_RESUME_MATRIX.json](07_QA验收/REI_P4B_RESUME_MATRIX.json) · [REI_P4B_ASSET_MANIFEST.json](07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- 生图能力边界实测：[AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)
