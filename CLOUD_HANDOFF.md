# CLOUD_HANDOFF.md｜Antigravity Cloud 云端接续交付手册

> **架构状态**：GitHub-first + Cloud Execution（本地开发迁移已完成并冻结，GitHub 私有仓库为唯一正式工程数据源）  
> **版本定位**：开发候选基线（**`P4-B PARTIAL`，非正式 `v1.0.0`**）

---

## 1. 仓库与已验证资产基线

| 字段 | 真值 |
| --- | --- |
| 唯一正式远程仓库 | `https://github.com/waynewayne893/rei-desktop-pet.git` |
| 仓库所有者与可见性 | `waynewayne893` / **`PRIVATE`**（严禁公开） |
| 目标分支 | `main` |
| **已验证资产基线 Commit SHA** | **`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`** |
| 候选标签 | `v0.4.0-p4b-candidate`（tag 对象 `e18bc9f086014f3c657ae3e4d334a145bc198556`，指向基线提交 `8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`） |
| 基线规模 | 600 个文件 / 104.95 MB / 0 凭据 / 0 受限 Codex 组件 / 474 张图片 0 条 EXIF 隐私元数据 |

---

## 2. 当前项目真实状态

- **P2**：`PARTIAL`（三套冻结原画与 P2 字节备份锁入基线；历史下载前上游来源继续记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可锁定（含白服 P3-FIX 派生母版、`188 px` 尺度、`(96, 195)` 脚底锚点）。
- **P4-A**：42 帧已齐备并受保护（白服 `idle/attempt-02` 透明修复已锁定；黑服新版 `running-right` 为 `FIX-BLACK` 且已明确人工验收通过；旧版黑服 `running-right` 为 `REJECTED` 已排除并留档）。
- **P4-B**：**171 帧标准动作候选已齐备**（校服 57 + 白服 57 + 黑服 57），三套 `1536×1872` 标准图集结构校验全部 `STRUCTURE_PASS`；**人工美术验收尚未全部完成**。
- **P4-B-FIX**：当前暂停——已完成 Antigravity 本地 `image-generator` 最小能力验证，结论 **`NATIVE_ALPHA_BLOCKED`**，等待主控裁定透明度替代管线与精确修复清单。
- **P4-C / P4-D / P5 / P6**：**均尚未获得执行授权**，禁止提前启动。

---

## 3. 云端环境初始化与依赖安装方法

在 Antigravity Cloud（Linux 容器）接入本仓库后执行：

```bash
git clone https://github.com/waynewayne893/rei-desktop-pet.git
cd rei-desktop-pet
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

依赖清单（[requirements.txt](requirements.txt)）：`Pillow>=11.0.0`（含 `libwebp`）、`numpy>=2.0.0`、`scipy>=1.14.0`。

---

## 4. 独立跨平台图集工具使用方法

云端环境无 Windows `OpenAI.Codex` MSIX 及 `hatch-pet` 专有组件（依法未随仓库分发），统一使用洁净自研跨平台工具 [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py)：

```bash
# 1. 一键核验冻结母版 + 派生母版 + 171 帧 + 三套标准图集（预期 exit 0, "ok": true）
python3 06_共用工具/rei_atlas_tools.py verify

# 2. 独立重装三套 1536x1872 标准图集并与仓库交付逐像素及 SHA-256 对拍
python3 06_共用工具/rei_atlas_tools.py reassemble --out-dir /tmp/rei-cloud-reassemble --write-sheets

# 3. 单独校验任意标准图集（1536x1872）或 v2 扩展图集（1536x2288）
python3 06_共用工具/rei_atlas_tools.py validate-atlas 03_校服绫波丽/P4-B/delivery/spritesheet-standard.png
```

---

## 5. 图像生成能力边界（已实测）

- **Antigravity 本地 `image-generator` 实测结论**：**`NATIVE_ALPHA_BLOCKED`**（证据见 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md) 与 [agy-image-gen-capability-test.json](07_QA验收/P4-B-FIX/capability-test/agy-image-gen-capability-test.json)）。
  - 强项：角色身份、服饰细节、Q 版比例与线稿还原极佳。
  - 硬缺口：仅输出不透明 RGB JPEG（无 `transparent_background: true`，要求透明会烤入棋盘格），且最宽画幅为 `16:9`（无 `3:1` 条带），被 `hatch-pet` 原生 Alpha 门禁拒绝 3/3。
- **工程约束**：未获主控正式裁定替代管线（方案 A：纯色色键底 + 2×3/2×4 网格 + 确定性抠图与明暗双底严检；或方案 B：外部原生 RGBA 生图通道）前，禁止擅自对不透明生图去背冒充原生透明条带。

---

## 6. 待人工验收动作与 `P4-B-FIX` 遗留事项

- **明确人工已验收 (`ACCEPTED`)**：仅黑服新版 `running-right`（8 帧，禁止重做）。
- **待人工美术验收 (`CANDIDATE`)**：其余 **163 帧**（P4-A 受保护基线 34 帧 + P4-B 新增 129 帧）。
- **离线 QA 重点提示复核的 3 处观察项**：
  1. `rei-school / waiting`（F6 举掌→F1 交握循环切回较直接）
  2. `rei-black / review`（F1–F4 扶臂、F5–F6 垂臂，循环回 F1 姿态切换）
  3. `rei-black / waving`（F1/F4 双臂放松垂放）
- **人工验收实图入口**：三套亮/暗底 9 行接触表（`03_*/04_*/05_*/P4-B/delivery/standard-contact-sheet*.png`）、18 个三形态同步对比 GIF（`07_QA验收/P4-B/comparison-gifs/` 与 `comparison-gifs-dark/`）、高分 `00`/`09` 胸前标识拼图（`07_QA验收/P4-B/p4b-chest-markings-qa-*.png`）。
- **`P4-B-FIX` 遗留事项**：等待主控下发两项裁定——① 透明度替代方案（方案 A/B）；② 精确重制动作清单。

---

## 7. 下一阶段云端任务入口（按顺序等待授权推进）

1. **云端首步｜Linux 云端独立恢复验证**（必做）：
   - 说明：T5-C 干净 Clone 测试在原 Windows 环境执行并全部通过，**仅代表远程仓库在当前本地环境可恢复，不代表 Linux 云端验证已完成**。
   - 用户在 Antigravity Cloud 接入本仓库后，第一步请在 Linux 容器内运行 `pip install -r requirements.txt`、`python3 06_共用工具/rei_atlas_tools.py verify` 与 `reassemble --out-dir /tmp/rei-cloud-check --write-sheets`，记录 Linux 实测输出。
2. **随后任务｜`REI-PET-REVIEW-CENTER-V1.0`**：在云端恢复验证通过后，按主控正式指令开发交互式人工审阅中心，协助用户高效完成 171 帧动态美术终审。
3. **后续排队｜`REI-PET-P4-B-FIX` → `P4-C` → `P4-D` → `P5`（回原 Windows 本地安装测试）→ `P6`**：均须严格等待主控逐阶段授权，禁止越权提前启动。

---

## 8. 本地工作区冻结声明

原有 Windows 本地工作区（`D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet`）自本交付起正式冻结：
- 完整保留，不删除；
- 停止日常本地开发，GitHub 私有仓库为唯一正式版本数据源；
- 本地仅作历史备份、必要预览及未来 P5 桌面宠物安装实测环境；
- 明日香参考工程与已安装 3 套明日香宠物继续严格只读保护。
