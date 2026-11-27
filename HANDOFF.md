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
- **当前阶段**：`P4-D_CANDIDATE_OFFLINE_QA_PASS`（`main` 已统一于 `44624e1`；`feat/p4d-final-assembly` 完成三套 v2 扩展图集装配、264 格离线 QA、独立与总交付包及 Windows P5 指南，待主控验收）。[P4-D QA 报告](07_QA验收/P4-D/P4D_QA_REPORT.md) · [P4-D 交付清单](08_正式交付/P4-D-candidate/P4D_DELIVERY_MANIFEST.json) · [Windows P5 指南](07_QA验收/P4-D/WINDOWS_P5_ACCEPTANCE_GUIDE.md)
- **云端核心环境**：`Ubuntu 24.04.5 LTS` / `Python 3.12.16` / 预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`），无 PyPI 访问（无 NumPy/SciPy），详见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- **图像生成实测边界**：全部 219 帧美术生产与人工验收均已完成，P4-D 零生图调用
- **未授权阶段**：P5 实机安装测试、P6 正式发布仍待主控对 P4-D 独立验收后逐阶段授权。

---

## 2. 接续顺序

1. 经用户授权将 `feat/p4d-final-assembly` 推送至 GitHub，由 ChatGPT 主控独立核验三套 v2 交付包、264 格离线 QA 与 SHA-256 清单。
2. 获主控 P5 授权后，在 Windows 本地按 [WINDOWS_P5_ACCEPTANCE_GUIDE.md](07_QA验收/P4-D/WINDOWS_P5_ACCEPTANCE_GUIDE.md) 执行原生 `validate_atlas.py --require-v2` 复检、三套独立安装、16 方向/死区/任务动画/重启持久化/Asuka 同尺寸对比实测。
3. 严禁未授权提前安装、修改 Asuka 或标记为正式 `v1.0.0`。

---

## 3. 核心交付文档索引

- 云端最终交接手册：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md)
- 云端恢复与环境锁：[CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) · [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)
- Windows 原生兼容性实测证据：[WINDOWS_COMPAT_TEST_REPORT.md](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_REPORT.md) · [WINDOWS_COMPAT_TEST_RESULT.json](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_RESULT.json) · [WINDOWS_NATIVE_VALIDATION_V2.json](07_QA验收/P4-COMPAT/WINDOWS_NATIVE_VALIDATION_V2.json)
- 云端环境与复算指南：[CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) · [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
- 项目实时状态与执行红线：[PROJECT_STATUS.md](PROJECT_STATUS.md) · [AGENTS.md](AGENTS.md)
- P4-B 接管、QA 与矩阵：[AGY_TAKEOVER_REPORT.md](07_QA验收/AGY_TAKEOVER_REPORT.md) · [REI_P4B_QA_REPORT.md](07_QA验收/REI_P4B_QA_REPORT.md) · [REI_P4B_RESUME_MATRIX.json](07_QA验收/REI_P4B_RESUME_MATRIX.json) · [REI_P4B_ASSET_MANIFEST.json](07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- 生图能力边界实测：[AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)
