# REI-PET-GIT-CLOUD-MIGRATION｜云端开发迁移首次提交预审报告 (`GIT_CLOUD_MIGRATION_PREFLIGHT`)

**预审结论：`PREFLIGHT_PASS`（所有工程完整性、安全/隐私/版权、体积、跨平台可恢复性及受限组件合规核验全部通过；当前已暂停于首次 Commit/Push 前，等待用户明确批准）。**

- **审计日期**：2026-11-27
- **架构路线**：Local-first → **GitHub-first + Cloud Execution**
- **本地来源**：`<LOCAL_PROJECT_ROOT>`（保留为历史备份与 P5 本地安装环境，未删除任何历史文件）
- **目标私有仓库**：`https://github.com/waynewayne893/rei-desktop-pet.git`（已只读核验：`visibility=PRIVATE`、`isPrivate=true`、`isEmpty=true`、未重复创建）
- **当前真实阶段**：`P4-B PARTIAL`（171 帧标准候选齐备，人工美术验收未全部完成；**非正式 `v1.0.0`**）
- **当前 Git 状态**：本地已 `git init -b main` 并绑定唯一 `origin`；**0 次 Commit、0 次 Push**

---

## 1. 拟上传文件及体积统计

| 目录 | 文件数 | 体积 (MB) | 包含内容 |
| --- | ---: | ---: | --- |
| `<ROOT>` | 9 | 0.04 | `.gitignore`、`README.md`、`AGENTS.md`、`PROJECT_STATUS.md`、`HANDOFF.md`、`requirements.txt`、`CLOUD_ENVIRONMENT.md`、`REPRODUCIBILITY.md`、`GIT_CLOUD_MIGRATION_PREFLIGHT.md` |
| `00_原始美术母版/` | 7 | 7.66 | 三套冻结原始母版 + `P2_字节备份/` + `REI_ART_FREEZE_MANIFEST.json` |
| `01_设计规范/` | 1 | 0.00 | `ASUKA_REUSE_MATRIX.md` |
| `02_标准化母版/` | 43 | 7.93 | P3 / P3-FIX 派生 RGBA 母版、尺度候选、构建脚本与工具合同 |
| `03_校服绫波丽/` | 143 | 27.80 | `rei-school` P4-A / P4-B 原始条带、57 帧候选、接触表、GIF、标准图集与校验 JSON |
| `04_白色战斗服/` | 144 | 25.97 | `rei-white` P4-A（含 `idle` 拒收件与修复件）/ P4-B 57 帧与标准图集交付 |
| `05_黑色战斗服/` | 168 | 23.61 | `rei-black` P4-A（含旧右跑拒收件与 FIX-BLACK 验收件）/ P4-B 57 帧与标准图集交付 |
| `06_共用工具/` | 2 | 0.01 | `rei_atlas_tools.py`（洁净跨平台校验/重装工具）+ `.gitkeep` |
| `07_QA验收/` | 75 | 11.92 | 全阶段门禁/QA/接管/预审报告、清单、3×9 恢复矩阵、18 个三形态 GIF、标识拼图、`P4-B-FIX` 生图能力实测留档 |
| `08_正式交付/` | 1 | 0.00 | `.gitkeep`（预留 P5 最终包目录，当前未进入 P5） |
| `09_项目文档/` | 7 | 0.02 | 路线图、动作规格、兼容性审计、P3 / P4-B / P4-C 交接文档 |
| **合计** | **600** | **~104.95 MB** | 完整可恢复工程基线 |

### 单文件体积与结构健康度
- **最大单文件**：`03_校服绫波丽/P4-B/originals/failed/attempt-01/source.png`（**2.59 MB**）。
- **超过 5 MB / 10 MB / 50 MB 文件数**：全部为 **0**（无需 Git LFS，远低于 GitHub 50 MB 警告线与 100 MB 硬上限）。
- **符号链接**：**0**；**异常 0 字节文件**：**0**（仅两处 `.gitkeep`）；**缓存垃圾**：**0**。

---

## 2. 排除文件及理由（`.gitignore`）

仓库通过根目录 [.gitignore](.gitignore) 仅排除运行期临时文件与本地凭据风险，**不排除任何有效工程素材、原始条带、拒收留档或 QA 证据**：

- `__pycache__/`、`*.py[cod]`、`$py.class`：Python 运行期字节码缓存，不可移植且无版本价值。
- `.DS_Store`、`Thumbs.db`、`desktop.ini`、`*.tmp`、`*.bak`、`*.swp`、`*~`：OS/编辑器临时文件。
- `.venv/`、`venv/`、`.env`、`.env.*`、`*.key`、`*.pem`：本地虚拟环境与敏感密钥隔离保护。
- **未纳入本仓库的外部目录**：`<LOCAL_ASUKA_ROOT>`（只读参考，严禁纳入或修改）、`C:\Users\<用户名>\.codex\pets`（本机已安装宠物）、`C:\Program Files\WindowsApps\OpenAI.Codex_*`（专有受限软件，见第 7 节）。

---

## 3. 敏感信息、隐私、版权与无关资产扫描

| 扫描项 | 结果 | 详情 |
| --- | :---: | --- |
| 凭据与密钥 (`sk-`, `AIza`, `ghp_`, `gho_`, `github_pat_`, `AKIA`, `Bearer`, `PRIVATE KEY`) | **0 命中** | 全库文本/JSON/MD/Python 零凭据泄露 |
| 邮箱地址 | **0 命中** | 正文零明文个人邮箱；Git 作者配置为 GitHub noreply 邮箱 |
| 隐私路径字符串（**请用户知情确认**） | 少量历史审计文本 | P2/P3/P4 历史 JSON/MD 审计证据中含有 Windows 本地路径（含用户名 `<用户名>` 及 `Codex_Asuka` / `.codex\pets` 审计路径），用于留痕隔离与来源追溯；因目标仓库已核验为 **`PRIVATE`** 且无任何凭据，保留原字节不破坏历史哈希 |
| 版权 / IP 提示 | **仅限私有仓库** | 角色造型基于 EVA 绫波丽二次创作，属于个人非公开桌面宠物工程；本仓库**必须永久保持 `PRIVATE`**，严禁公开或二次分发 |
| 无关资产 | **0** | 全部 600 个文件均为 Rei Desktop Pet 合法工程资产、证据或入口文档 |

---

## 4. 工程资产完整性核验

已使用洁净跨平台脚本 `python 06_共用工具/rei_atlas_tools.py verify` 完成实测核验（退出码 `0`，`"ok": true`）：

- 三套冻结原始母版 + P2 字节备份：6/6 哈希完全一致，原字节未修改。
- 三套 P3 / P3-FIX 派生 RGBA 母版：3/3 哈希完全一致。
- P4-A 受保护 42 帧（含白服修复与黑服 FIX-BLACK）+ P4-B 129 帧 = **171/171 帧**全部通过哈希、`192×208 RGBA`、边框留白、零隐藏 RGB 与单一 8 连通分量检查。
- 三套 `1536×1872` 标准图集：3/3 哈希完全一致，57 有效格 + 15 全透明空格结构校验 0 error / 0 warning。
- 历史拒收件（白服 `idle/attempt-01`、黑服旧 `running-right`）及 Antigravity 生图能力测试（3 份原图 + JSON + 报告）均完整保留。
- 明日香参考工程（`HEAD = 1e52fc5c20b947a2570695f94c968990c32fd025`，`diff_sha256 = 9a952faa6ae913af0377e5d44a65be422f69a19d0589b173fe884d2c82db868b`）与已安装 3 套明日香宠物 100% 未改动。

---

## 5. 跨平台依赖风险审计

| 风险项 | 涉及文件 | 影响与缓解 |
| --- | --- | --- |
| Windows 硬编码字体 `C:/Windows/Fonts/consola.ttf` | 4 个历史脚本（`build_static_masters.py`、`build_p3_fix.py`、`build_preview_row.py`、`assemble_delivery.py`） | 在 Linux 云端直接执行历史脚本会触发字体路径报错；历史脚本按原字节保留审计，云端改用内置跨平台字体回退的 `06_共用工具/rei_atlas_tools.py` |
| Windows `OpenAI.Codex` MSIX 依赖 | 3 个历史脚本（`build_preview_row.py`、`build_rows.py`、`assemble_delivery.py`） | Linux 云端无 MSIX 包；云端由 `06_共用工具/rei_atlas_tools.py` 独立替代 |
| 历史清单中的反斜杠路径字段 | `REI_ART_FREEZE_MANIFEST.json`、`REI_P3_ASSET_MANIFEST.json` | 仅作只读溯源记录；`rei_atlas_tools.py` 统一按仓库相对路径与 `filename` 解析，已在代码中规避平台路径分隔符问题 |
| 中文字段与目录名 | `00_原始美术母版` 等 | 已设 `core.quotepath false`，Linux/Git UTF-8 完整兼容 |

---

## 6. 云端可恢复性判断：**`HIGH / VERIFIED`**

实测运行 `python 06_共用工具/rei_atlas_tools.py verify` 与 `reassemble`（独立临时输出目录），结果如下：
- **171/171 帧与三套冻结/派生母版校验**：`"ok": true`，`errors: []`；
- **三套标准图集独立重装对拍**：
  - `rei-school`：`validation_ok=true`，`pixel_identical_to_committed=true`，`sha256_identical=true`（`59fe359e31ee208d...`）
  - `rei-white`：`validation_ok=true`，`pixel_identical_to_committed=true`，`sha256_identical=true`（`8dc945e110fefa5f...`）
  - `rei-black`：`validation_ok=true`，`pixel_identical_to_committed=true`，`sha256_identical=true`（`e7bf03bb0f933a11...`）

结论：在任意安装 `Python 3.11+` 与 `requirements.txt` 的 Linux 云端环境中，**无需 Windows、无需 Codex MSIX、无需 `hatch-pet`**，即可从本 GitHub 私有仓库 100% 恢复全部 171 帧、验证全部哈希并逐字节无差重装三套标准图集。

---

## 7. 无法直接迁移的组件及解决方案

| 受限组件 | 无法直接迁移的原因 | 解决方案 |
| --- | --- | --- |
| Windows `OpenAI.Codex 26.1120.6357.0` 随附 `hatch-pet/scripts/*` | 属于 Windows MSIX 专有应用内部组件，包内无开源再分发许可，依法不得复制到本仓库 | 1. 在 `AGY_TOOLCHAIN_CAPABILITY.json` 与 `REI_P3_TOOLCHAIN_EVIDENCE.md` 锁定其版本与 SHA-256；2. 云端全部使用洁净自研的 `06_共用工具/rei_atlas_tools.py` 独立实现校验与装配；3. 最终 P5 安装前于原 Windows 环境只读跑官方 `validate_atlas.py --require-v2` 做最终双验 |
| 原生 RGBA 图像生成能力 (`transparent_background: true`) | Antigravity 原生 `image-generator` 实测仅输出不透明 RGB JPEG（`16:9`），当前为 `NATIVE_ALPHA_BLOCKED` | 迁移阶段不依赖新生成图；后续云端执行 `P4-B-FIX` / `P4-C` 前，按主控裁定启用方案 A（纯色色键底 + 网格布局 + 确定性抠图与明暗双底严检）或方案 B（外部原生 RGBA 通道） |
| Codex Desktop 浮窗真实运行与注册验收（P5） | 依赖 Windows 本机 `OpenAI.Codex` 客户端与 `C:\Users\<user>\.codex\pets` | 明确界定为 P5 最终本地收尾步骤，云端完成全部生产、校验、WebP 打包与 QA 后再拉回原 Windows 机器注册实测 |

---

## 8. T5 / T6 执行计划（待用户明确批准后启动）

请用户审阅本报告并明确批准首次 Commit 及 Push。获准后将立即依次执行：
1. **T5**：提交当前 600 文件开发候选基线（标记为 `P4-B PARTIAL`，非 `v1.0.0`）并常规推送至 `origin main` → 核验远程仍 `PRIVATE` 与本地/远端 Commit SHA 一致 → 在独立目录执行干净 `git clone` 恢复测试，运行 `rei_atlas_tools.py verify` 与 `reassemble` 核对输出与哈希；
2. **T6**：写入包含已验证 Commit SHA 与完整云端接续指南的 `CLOUD_HANDOFF.md`，提交推送后停止，交由用户在 Antigravity Cloud 接入执行云端恢复验证。
