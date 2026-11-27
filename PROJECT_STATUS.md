# PROJECT_STATUS.md｜Rei Desktop Pet 真实项目状态

- **更新时间**：2026-11-27
- **执行模式**：**GitHub-first + Cloud Execution**（本地开发迁移已完成并正式冻结）
- **唯一正式私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（Owner：`waynewayne893`，`PRIVATE`，分支 `main`）
- **已验证远程资产基线 Commit SHA**：`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（候选标签 `v0.4.0-p4b-candidate`）
- **版本定位**：开发候选基线（**`P4-B PARTIAL`，非正式 `v1.0.0`**）

---

## 1. 当前真实阶段状态（严格以实证为准）

- **P2**：`PARTIAL`（原工程只读审计、三套冻结原画与 P2 字节备份、十目录骨架及复用矩阵基线已接受；历史下载前上游来源继续记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可锁定（三套 1024×1536 RGBA 派生母版，白服采用 P3-FIX 修复版，`188 px` 尺度与 `(96, 195)` 脚底锚点锁定）。
- **P4-A**：**42 帧已齐备**并受哈希保护（含白服 `idle/attempt-02` 透明修复版与黑服 `FIX-BLACK` 新版 `running-right`；黑服新版右跑已明确人工验收通过，旧版右跑标记 `REJECTED` 排除）。
- **P4-B**：**171 帧标准动作候选已齐备**（每套 57 帧 × 3 形态），三套 `1536×1872` 标准图集通过官方 `validate_atlas.py` 与洁净跨平台工具 `06_共用工具/rei_atlas_tools.py` 双重校验。
- **P4-B 人工美术验收**：**尚未全部完成**（明确 `ACCEPTED` 8 帧，其余 163 帧为 `CANDIDATE` 待人工动态美术终审；QA 提示重点关注 `rei-school / waiting`、`rei-black / review`、`rei-black / waving`）。
- **P4-B-FIX**：当前暂停——等待主控裁定透明度替代管线与精确修复清单，未改动 171 帧基线。
- **Antigravity 本地 `image-generator` 实测结果**：**`NATIVE_ALPHA_BLOCKED`**（仅输出不透明 RGB JPEG、最大 `16:9`、无 `transparent_background: true`），详见 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)。
- **GitHub 私有仓库迁移（本地侧 T1–T6）**：**已完成**（600 文件 / 104.95 MB 已常规推送至 `Private` 仓库 `main` 并打候选标签 `v0.4.0-p4b-candidate`；独立临时目录干净 Clone 运行 `verify` 与 `reassemble` 全部通过且三套标准图集 SHA-256 逐字节一致；**注意：仅代表本地环境可恢复，Linux 云端独立恢复验证尚未执行**）。
- **P4-C / P4-D / P5 / P6**：**尚未获得执行授权**，均未启动。

---

## 2. 下一步任务队列（转入 Antigravity Cloud 执行）

1. **Linux 云端独立恢复验证**（用户于 Antigravity Cloud 接入本仓库后首步运行 `rei_atlas_tools.py verify` 与 `reassemble`）。
2. **`REI-PET-REVIEW-CENTER-V1.0`**：开发人工审阅中心辅助完成 171 帧终审。
3. **`REI-PET-P4-B-FIX`**：待主控裁定透明度替代管线与精确修复清单后执行。
4. **`P4-C` / `P4-D` / `P5`（回原 Windows 本地安装实测） / `P6`**：等待逐阶段授权。

详见：[CLOUD_HANDOFF.md](CLOUD_HANDOFF.md) · [GIT_CLOUD_MIGRATION_FINAL_REPORT.md](GIT_CLOUD_MIGRATION_FINAL_REPORT.md)
