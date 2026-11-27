# PROJECT_STATUS.md｜Rei Desktop Pet 真实项目状态

- **更新时间**：2026-11-27
- **执行模式**：GitHub-first + Cloud Execution（云端迁移预审中）
- **唯一目标私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（`Private`，空分支，**尚未 Commit / Push**）
- **版本定位**：开发候选基线（**`P4-B PARTIAL`，非正式 `v1.0.0`**）

---

## 1. 当前真实阶段状态（严格以本地实证为准）

- **P2**：`PARTIAL`（原工程只读审计、三套母版冻结与字节备份、十目录骨架及复用矩阵基线已接受；历史下载前上游路径仍记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可并锁定（三套 1024×1536 RGBA 派生母版，白服采用 P3-FIX 修复版，`188 px` 候选尺度与 `(96, 195)` 脚底锚点锁定）。
- **P4-A**：**42 帧已齐备**并受哈希保护（含白服 `idle/attempt-02` 透明修复版与黑服 `FIX-BLACK` 新版 `running-right`；黑服新版右跑已明确人工验收通过，旧版右跑已标记 `REJECTED` 排除）。
- **P4-B**：**171 帧标准动作候选已齐备**（每套 57 帧 × 3 形态），三套 `1536×1872` 标准图集均通过官方 `validate_atlas.py` 及洁净跨平台工具 `06_共用工具/rei_atlas_tools.py` 校验（0 error / 0 warning，且跨平台重装 SHA-256 逐字节一致）。
- **P4-B 人工美术验收**：**尚未全部完成**（明确 `ACCEPTED` 8 帧，其余 163 帧为 `CANDIDATE` 待人工动态美术终审；此前 QA 重点提示 3 处观察项：`rei-school / waiting`、`rei-black / review`、`rei-black / waving`）。
- **P4-B-FIX**：以实际最新测试结果为准——已完成 Antigravity `image-generator` 最小能力验证，状态为 **`NATIVE_ALPHA_BLOCKED`**，已暂停并等待主控裁定透明度替代管线与精确修复清单，未改动既有 171 帧。
- **Antigravity 图片生成能力**：以实测证据 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md) 为准——角色身份还原优秀，但仅输出不透明 RGB JPEG（无 `transparent_background: true`，最大 `16:9`），未通过 `hatch-pet` 原生 Alpha 门禁。
- **P4-C / P4-D / P5 / P6**：**尚未获得执行授权**，均未启动。

---

## 2. 三套标准图集与冻结母版哈希真值

| 形态 | 冻结原画 SHA-256 | 标准 1536×1872 图集 SHA-256 | 跨平台重装对拍 |
| --- | --- | --- | :---: |
| `rei-school` | `68d79674728e46b1bbff62070b9e57c79ad6e3b9f70354a344539b26511b0bc1` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` | `sha256_identical: true` |
| `rei-white` | `ec683e7185e0399494a1f5be1ff6de74f7187c22999bc72b7daded626b179019` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` | `sha256_identical: true` |
| `rei-black` | `be5907538ecbade28ed82ba8236c5fd461b119f5ef928a1289d7488429aed7cb` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` | `sha256_identical: true` |

---

## 3. 当前门禁状态

- **已完成**：T1 全量迁移审计、T2 跨平台洁净工具与许可梳理、T3 统一云端入口七件套、T4 [GIT_CLOUD_MIGRATION_PREFLIGHT.md](GIT_CLOUD_MIGRATION_PREFLIGHT.md)。
- **当前暂停点**：等待用户明确批准首次 Commit 和 Push，获准后立即执行 T5（推送 + 独立目录干净 Clone 恢复与重装验证）与 T6（产出 `CLOUD_HANDOFF.md`）。
