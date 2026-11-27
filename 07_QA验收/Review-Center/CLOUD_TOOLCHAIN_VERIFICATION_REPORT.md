# CLOUD_TOOLCHAIN_VERIFICATION_REPORT.md｜统一云端工具链复验报告（T2）

- **任务编号**：`REI-PET-CLOUD-P4B-REVIEW`（T2）
- **开发分支**：`feat/p4b-review-center-v1`（基于 T1 结项基线 `b51100a162eaea16bd7237878d801733b623f4c4`）
- **验证日期**：2026-11-27
- **验证结论**：**`UNIFIED_TOOLCHAIN_PASS`（零外置依赖、原资产零修改、三套标准图集跨平台逐字节一致）**

---

## 1. 统一架构与去重变更

| 文件 | 变更性质 | 说明 |
| --- | --- | --- |
| [06_共用工具/rei_atlas_tools.py](../../06_共用工具/rei_atlas_tools.py) | **升级为唯一主入口** | 全面迁移至 **Python 标准库 + 预装 Pillow** 单核心实现，统一承载 `verify`、`validate-atlas`（含 `--require-v2`）、`reassemble` 与 `build-compat` 全部四项子命令，消除对 PyPI `numpy`/`scipy` 的硬依赖 |
| [06_共用工具/rei_compat_builder.py](../../06_共用工具/rei_compat_builder.py) | **收敛为轻量兼容别名** | 仅保留 50 行符号重导出与 CLI 委托，指向 `rei_atlas_tools.py`，消除约 1,000 行重复代码，同时 100% 保留 `REI-PET-CLOUD-BOOTSTRAP` 历史命令与可追溯性 |
| [06_共用工具/build_review_center.py](../../06_共用工具/build_review_center.py) | **新增（纯标准库）** | 从 `REI_P4B_ASSET_MANIFEST.json` 与 `REI_P4B_RESUME_MATRIX.json` 确定性生成 Review Center V1.0 数据包、模板与离线 ZIP |
| [requirements.txt](../../requirements.txt) | **对齐云端真值** | 仅声明必需核心依赖 `Pillow>=11.0.0`，将 `numpy`/`scipy` 标注为仅历史 Windows 归档脚本可选依赖 |
| 历史 Windows 阶段脚本（5 份） | **原字节保留** | `build_static_masters.py`、`build_p3_fix.py`、`build_preview_row.py`、`build_rows.py`、`assemble_delivery.py` 零改动留档 |

---

## 2. 云端安全与环境锁合规核验

- **网络权限**：未扩大云端网络访问权限，未启用 Turbo 模式，全程零 PyPI / 外部下载。
- **实测锁定运行环境**（详见 [CLOUD_RUNTIME_LOCK.txt](../../CLOUD_RUNTIME_LOCK.txt)）：
  - OS：`Ubuntu 24.04.5 LTS`（`Linux 6.18.57 x86_64`, `glibc 2.39`）
  - Python：`3.12.16`
  - Pillow：`13.0.0`（内置 `libwebp 1.6.0`、`zlib 1.3`、`freetype2 2.14.3`）
  - NumPy / SciPy：`NOT_INSTALLED`（不再需要）
- **最终平台门禁保留声明**：Windows 本机 `OpenAI.Codex` 内置 `hatch-pet\scripts\validate_atlas.py --require-v2` 始终保留为最终桌面交付平台门禁，严禁拷贝至本仓库。

---

## 3. 复验实测结果（全部 EXIT=0）

### 3.1 `python3 06_共用工具/rei_atlas_tools.py verify`
- **退出码**：`0` · `"ok": true` · `"engine": "unified-stdlib-pillow"`
- `verified_frozen_and_backups`: **`6`**（3 套冻结原画 + 3 份 `P2_字节备份/` 哈希 100% 一致）
- `verified_derived_masters`: **`3`**（3 套 P3 / P3-FIX 派生母版哈希 100% 一致）
- `verified_frames`: **`171`**（全部 171 帧哈希、`192×208 RGBA`、1px 边框留白、0 透明隐藏 RGB、单一 8 连通前景主体 100% 通过）
- `verified_atlases`: **`3`**（三套 `1536×1872` 标准图集 57 有效格 + 15 全透明空格、0 透明 RGB 残留 100% 通过）
- `errors`: `[]`

### 3.2 `python3 06_共用工具/rei_atlas_tools.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets`
- **退出码**：`0` · `"ok": true`

| 形态 | 校验 | 像素一致 | 文件字节 | 重装 PNG SHA-256 | 与仓库基线 SHA-256 一致 |
| --- | :---: | :---: | ---: | --- | :---: |
| `rei-school` | PASS | **TRUE** | `1,076,432` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` | **TRUE** |
| `rei-white` | PASS | **TRUE** | `1,108,217` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` | **TRUE** |
| `rei-black` | PASS | **TRUE** | `990,796` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` | **TRUE** |

### 3.3 附加验证
- `python3 06_共用工具/rei_atlas_tools.py validate-atlas 07_QA验收/P4-COMPAT/rei-compat-test/spritesheet.webp --require-v2` → 退出码 `0`，`ok: true`，`74` 有效格 + `14` 空格，`0` 透明 RGB 残留，`errors: []`。
- `python3 06_共用工具/rei_compat_builder.py verify`（历史别名验证）→ 退出码 `0`，`ok: true`，`verified_frames: 171`，`errors: []`。
- **原始资产零修改确认**：`00_原始美术母版/`、`02_标准化母版/`、`03_校服绫波丽/`、`04_白色战斗服/`、`05_黑色战斗服/` 全部文件零修改。
