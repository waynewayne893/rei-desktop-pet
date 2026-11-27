# PROJECT_STATUS.md｜Rei Desktop Pet 真实项目状态

- **更新时间**：2026-11-27
- **执行模式**：**GitHub-first + Cloud Execution**（本地开发迁移已完成并正式冻结）
- **唯一正式私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（Owner：`waynewayne893`，`PRIVATE`，分支 `main`）
- **已验证初始资产基线 Commit SHA**：`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（候选标签 `v0.4.0-p4b-candidate`）
- **兼容性预验证分支 Commit SHA**：`6dc14434c1fcaf82ed1a0f996a6a9142b4f5892d`（由 `cloud-bootstrap/p4-compat-preverify` 交付并已包含于试验分支历史。结项核验时远端 `main` 仍指向 `0b430a2`）
- **原生兼容性主控裁定（`REI-P4-COMPAT-MAIN-REVIEW-02`）**：**`BASE_RUNTIME_COMPATIBILITY_PASS`** / **`DETAILED_RUNTIME_VERIFICATION_PARTIAL`**
- **版本定位**：`P4-B_ART_ACCEPTANCE_PASS`，尚未进行正式发布

---

## 1. 当前真实阶段状态（严格以实证为准）

- **P2**：`PARTIAL`（原工程只读审计、三套冻结原画与 P2 字节备份、十目录骨架及复用矩阵基线已接受；历史下载前上游来源继续记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可锁定（三套 1024×1536 RGBA 派生母版，白服采用 P3-FIX 修复版，`188 px` 尺度与 `(96, 195)` 脚底锚点锁定）。
- **P4-A**：**42 帧已齐备**并受哈希保护（含白服 `idle/attempt-02` 透明修复版与黑服 `FIX-BLACK` 新版 `running-right`；黑服新版右跑 8 帧已明确人工验收通过，旧版右跑标记 `REJECTED` 排除）。
- **P4-B**：**171 帧标准动作候选已齐备**（每套 57 帧 × 3 形态），三套 `1536×1872` 标准图集通过官方 `validate_atlas.py` 与云端跨平台校验器双重校验。
- **P4-B 人工美术验收**：正式 27/27 动作、171/171 帧 `ACCEPTED`。待审、需修复和拒收均为 0。归档包含原始验收 JSON 与资产绑定。 [人工验收台账](07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json)
- **Codex Cloud 专项试验**：校服 waiting 六帧和黑服四方向均人工通过，裁定 `CODEX_CLOUD_ART_PIPELINE_QUALIFIED`。新版 waiting 保留为已通过备用候选，正式图集沿用现有帧。用户曾提出预览画质疑问，最终接受全部正式动作。本批裁定不含全量锐化、超分辨率或重新生成。
- **Linux 云端独立恢复验证（`REI-PET-CLOUD-BOOTSTRAP` T0–T1）**：**已接受**（在 `Ubuntu 24.04.5 LTS` / `Python 3.12.16` / 预装 `Pillow 13.0.0` + `libwebp 1.6.0` + `zlib 1.3` 下，使用零外置依赖工具 [rei_compat_builder.py](06_共用工具/rei_compat_builder.py) 完成 6/6 冻结与备份、3/3 派生母版、171/171 帧与 3/3 标准图集复算，三套重装标准图集与 Windows 基线 **100% 像素一致且 PNG SHA-256 逐字节一致**；详见 [CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) 与 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)）。
- **P4-COMPAT 原生兼容性预验证（`rei-compat-test`）**：**`BASE_RUNTIME_COMPATIBILITY_PASS` / `DETAILED_RUNTIME_VERIFICATION_PARTIAL`**（依据 `REI-P4-COMPAT-MAIN-REVIEW-02`）：
  - **已实证通过项**：临时 v2 测试包三文件 SHA-256 独立复算一致；Windows 原生 `OpenAI.Codex 26.1120.6357.0` `validate_atlas.py --require-v2` 退出码 `0`、0 错误、0 警告；Linux 离线 QA 与 Windows 原生 QA 共 88 格逐项对应无差异；用户亲自在 Codex Desktop 完成运行测试确认无异常；安全回退后原有 3 套 Asuka 宠物共 6 个文件安装前后 SHA-256 完全一致。详见 [WINDOWS_COMPAT_TEST_REPORT.md](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_REPORT.md) 与 [WINDOWS_COMPAT_TEST_RESULT.json](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_RESULT.json)。
  - **严格未标通过的细项边界**：16 方向逐项映射读数、`R0C6` 中性参考格中心死区实际显示行为（`NEUTRAL_CELL_0_6` vs `IDLE_FALLBACK`）、完全退出重启持久化、以及任务/事件触发动画（`waving`、`jumping`、`failed`、`waiting`、`running`、`review`）均尚未完成逐项实测，留待后续专项验证或 P5 终验，**不得标记为已全部通过**。
  - 临时方向测试素材严格隔离于 `07_QA验收/P4-COMPAT/`，不计入正式 P4-C 产物。
- **Antigravity 本地 `image-generator` 实测结果**：**`NATIVE_ALPHA_BLOCKED`**（仅输出不透明 RGB JPEG、最大 `16:9`、无 `transparent_background: true`），详见 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)。
- **后续裁定**：`P4-B-FIX_SKIPPED`、`P4-C_PRODUCTION_AUTHORIZED`。远端 main 已核验统一基准 `6b4229f`。独立 P4-C 任务分支完成 48 帧结构检查，其中黑服 4 帧保留人工通过，44 帧待人工终审。P4-D、P5、P6 仍待逐阶段授权。

---

## 2. 当前任务队列

1. 统一结项提交包含兼容性预验证、Review Center、Codex Cloud 专项试验和两份原始人工验收记录。 [远端 fast-forward 方案](07_QA验收/P4-B/human-acceptance/CLOSEOUT_AND_MAIN_FF_PLAN.md)
2. P4-C 已在独立任务分支完成 48 帧离线 QA。待批后推送该分支，44 新帧待人工验收。 [P4-C 方向候选 QA](07_QA验收/P4-C/P4C_PRODUCTION_QA_REPORT.md)
3. P4-D、P5、P6 等待逐阶段授权。

详见：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md) · [CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) · [WINDOWS_COMPAT_TEST_REPORT.md](07_QA验收/P4-COMPAT/WINDOWS_COMPAT_TEST_REPORT.md)
