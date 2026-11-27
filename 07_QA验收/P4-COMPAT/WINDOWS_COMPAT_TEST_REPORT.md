# WINDOWS_COMPAT_TEST_REPORT.md｜Windows Codex Desktop Pets v2 原生兼容性实测报告

- **任务代号**：`REI-PET-P4-COMPAT-WINDOWS` / `REI-PET-P4-COMPAT-WINDOWS-CLOSEOUT`
- **测试包标识**：`rei-compat-test`（`custom:rei-compat-test`，**临时兼容性预验证包，非正式 P4-C / P4-D / P5 发布件**）
- **固定测试来源**：
  - 仓库：`https://github.com/waynewayne893/rei-desktop-pet`（`Private`）
  - 分支：`cloud-bootstrap/p4-compat-preverify`
  - 基线 Commit：`c5b5b4ffaae6db2c13c75c64e14918f6b0c7858a`
- **执行时间（本机）**：`2026-11-27 06:21:00` – `06:53:27`
- **综合判定（保守口径）**：**`PARTIAL`（无阻断性错误；全部机器/原生 v2 门禁、Codex Desktop 识别加载、用户总体无异常确认及 Asuka 隔离回退均通过；未逐项回报或未执行的细目严格未标记为 `PASS`）**

---

## 1. 测试环境与工具链实录

| 项目 | 实测值 |
| --- | --- |
| Windows OS | `Microsoft Windows 11 家庭中文版 10.0.22000 (Build 22000)` |
| Codex Desktop MSIX | `OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0` |
| Codex Desktop 版本 | `26.1120.6357.0` |
| 原生校验器路径 | `C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0\app\resources\skills\skills\.curated\hatch-pet\scripts\validate_atlas.py` |
| Python / Pillow / libwebp | `Python 3.14.6` / `Pillow 12.3.0` / `libwebp 1.6.0` |
| 独立临时 Git 克隆目录 | `%TEMP%\rei-compat-win-git`（原本地开发目录 `D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet` 全程未改动） |
| 独立临时解包测试目录 | `%TEMP%\rei-compat-download` |

---

## 2. T1｜下载、SHA-256 核验与原生 `validate_atlas.py --require-v2` 校验（PASS）

### 2.1 三文件 SHA-256 核对（3/3 精确一致）

| 文件 | 体积 (Bytes) | 实测 SHA-256 | 清单比对 |
| --- | ---: | --- | :---: |
| `rei-compat-test.zip` | `803,543` | `9b36d7dd843aa65e76d17b7da63f876681edacbd9b23f7963bdf50b06e834fea` | **MATCH** |
| `rei-compat-test/pet.json` | `349` | `f48cbc7e785e39698ad5f701fabd6556917be72e7b3bee7ddae036b0ad27913f` | **MATCH** |
| `rei-compat-test/spritesheet.webp` | `802,834` | `bd6d29f401738015dddf452a79ffc460e6d53851f1ce691cbf25dd4605365201` | **MATCH** |

### 2.2 原生 `validate_atlas.py --require-v2` 输出

- **退出码**：`0`
- **完整 88 格校验 JSON**：见 [WINDOWS_NATIVE_VALIDATION_V2.json](WINDOWS_NATIVE_VALIDATION_V2.json)
- **标准输出摘要**：
```json
{
  "ok": true,
  "format": "WEBP",
  "mode": "RGBA",
  "columns": 8,
  "rows": 11,
  "sprite_version_number": 2,
  "width": 1536,
  "height": 2288,
  "transparent_rgb_residue_pixels": 0,
  "errors": [],
  "warnings": []
}
```
- **关键结构确认**：
  - `R0C6`（行 0 列 6 中性参考格）被官方校验器识别为有效格（`used: true, nontransparent_pixels: 7509`），**未触发**历史 Asuka v2 包曾出现的 `idle row 0 column 6 is empty or too sparse` 错误；
  - 第 9–10 行共 16 个方向格全部有效（`9467–9543 px`）；
  - 14 个预留空格全部为 `0 px`；
  - `transparent_rgb_residue_pixels = 0`，`errors = []`，`warnings = []`。

---

## 3. T2–T3｜预审、用户授权安装与实机观测结果

### 3.1 安装前预审与授权
- 目标目录 `%USERPROFILE%\.codex\pets\rei-compat-test` 安装前确认不存在（`False`）。
- 既有宠物目录仅包含 `asuka-school`、`asuka-work`、`asuka-mixed-test`，安装前当前选中宠物经 Codex 本地状态核查为 `custom:asuka-school`。
- 获得用户明确回复 **“批准安装”** 后，于 `2026-11-27 06:23:59` 仅创建独立目录 `rei-compat-test` 并复制 `pet.json` 与 `spritesheet.webp`，安装后复核两文件 SHA-256 100% 一致，且全部 6 个 Asuka 文件哈希零变化。

### 3.2 Codex Desktop 运行时取证与用户实测结论

1. **已客观证实的运行时兼容性事实（PASS）**：
   - 用户已亲自在 Codex Desktop 中完成临时宠物兼容性测试，并明确确认 **“未发现问题”**。
   - Codex Desktop `26.1120.6357.0` 本地 SQLite 状态（已脱敏，不含账号/凭据信息）独立佐证：
     - 成功识别本地测试包 `custom:rei-compat-test`；
     - 成功缓存其 `spriteVersionNumber = 2`、`1536×2288` 图集指纹；
     - 在 `first-awake-pet-notification-avatar-ids` 中记录了 `custom:rei-compat-test`；
     - 浮窗坐标产生实际拖动位移（`x: 1123→1104, y: 46→87`）；
     - 测试结束后活动宠物已切回 `custom:asuka-school`。
   - **附带架构发现（对正式 P5 安装/清理有重要参考价值）**：Codex Desktop `26.1120.6357.0` 在读取 `%USERPROFILE%\.codex\pets\<id>` 后，会自动将本地自定义宠物迁移同步为云端宠物条目（记录在 `migrated-cloud-pet-ids-v1`）。因此后续正式发布/测试卸载时，除移除本地目录外，若 UI 中仍保留云端同步副本，需由用户在 Codex UI 中按需移除。

2. **未逐项回报 / 未触发 / 未执行项目（严格不标为 `PASS`）**：
   - **明暗背景边缘、裁切与待机循环（`R0C0–R0C5` vs `R0C6`）**：用户确认总体未发现问题，但未分项汇报各项细目，因此在 JSON 中保留 `null`（不臆测标为 `PASS`）。
   - **左右拖动动画（`running-right` / `running-left`）**：虽有浮窗位移记录且用户未发现问题，但未分别回报左右向细节，记为 `NOT_ITEMIZED`。
   - **任务/事件触发动画（`waving` / `jumping` / `failed` / `waiting` / `running` / `review`）**：用户未回报具体触发观测，全部严格记为 **`NOT_TRIGGERED`**。
   - **鼠标 16 方向扇区逐格核对与中心死区 `R0C6` 行为**：用户总体确认未发现问题，但未分别提供 16 扇区读数或明确指出正中心死区显示的是 `NEUTRAL_CELL_0_6` 还是 `IDLE_FALLBACK`，全部严格记为 **`NOT_REPORTED`**（中心死区运行时真值待后续专项观察或由用户补充确认）。
   - **完全退出重启持久化**：收口阶段（`06:53:23`）进程核查显示，本机全部 `OpenAI.Codex` 进程启动时间仍为 `2026-11-27 04:48:48–04:53:20`（早于 `06:23:59` 安装时间），说明本轮未执行完全退出后重启，记为 **`codex_fully_quit_and_relaunched: false`**。

---

## 4. T4｜安全回退与 6 个 Asuka 文件 SHA-256 完整性证据（PASS）

- **本地临时测试宠物清理**：于 `2026-11-27 06:53:27` 仅删除 `%USERPROFILE%\.codex\pets\rei-compat-test`，复核 `Test-Path = False`，剩余目录仅保留 `asuka-school`、`asuka-work`、`asuka-mixed-test`。
- **6 个 Asuka 文件安装前 vs 回退后 SHA-256 对照（6/6 逐字节一致）**：

| 文件 | 体积 (Bytes) | 安装前 SHA-256 | 回退后 SHA-256 | 比对 |
| --- | ---: | --- | --- | :---: |
| `asuka-school/pet.json` | `248` | `8f22978ed8105d6b6e023377a5d550406fd220f3cdaeb59dbd429393366e7091` | `8f22978ed8105d6b6e023377a5d550406fd220f3cdaeb59dbd429393366e7091` | **UNCHANGED** |
| `asuka-school/spritesheet.webp` | `1,971,788` | `51ecce0097b08e17308cbc90bb4dbf8c7353cabb90e33caf970b8d9a8fe80c29` | `51ecce0097b08e17308cbc90bb4dbf8c7353cabb90e33caf970b8d9a8fe80c29` | **UNCHANGED** |
| `asuka-work/pet.json` | `258` | `0dc5f4aa2a1c4accb0e0fc63ba0ca2cc5fa289f5195b0cf0885ae8454a43aa25` | `0dc5f4aa2a1c4accb0e0fc63ba0ca2cc5fa289f5195b0cf0885ae8454a43aa25` | **UNCHANGED** |
| `asuka-work/spritesheet.webp` | `2,017,070` | `0d4024945ca4d5f757eff9afa6c0eb9f1892eadb93f8fdef5ae317c23de45049` | `0d4024945ca4d5f757eff9afa6c0eb9f1892eadb93f8fdef5ae317c23de45049` | **UNCHANGED** |
| `asuka-mixed-test/pet.json` | `301` | `8fd1de1dd21b142947c71da042b8e65465c76bc9cb896ad3ab6ce55fdbbdba04` | `8fd1de1dd21b142947c71da042b8e65465c76bc9cb896ad3ab6ce55fdbbdba04` | **UNCHANGED** |
| `asuka-mixed-test/spritesheet.webp` | `1,988,930` | `83aba65992452114a6a4156f6ec9655a3869b3a127b6ab0ce8edf15ccc865fcb` | `83aba65992452114a6a4156f6ec9655a3869b3a127b6ab0ce8edf15ccc865fcb` | **UNCHANGED** |

- **原本地开发工程完整性**：`D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet` 全程未改动（`main...origin/main`，工作树干净）。

---

## 5. 边界声明

- 本报告仅记录 `rei-compat-test` 临时兼容性预验证包的 Windows 原生实测与隔离回退证据。
- 本轮未生成任何新动画素材，未修改 `main` 分支，未合并分支，未启动 `P4-B-FIX`、正式 `P4-C`、`P4-D`、`P5` 或 `P6`。
- 最终兼容性结论及后续阶段授权交由 ChatGPT 主控基于本报告及结构化结果 JSON 独立裁定。
