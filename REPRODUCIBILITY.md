# REPRODUCIBILITY.md｜独立环境恢复与复算指南

本指南说明如何在任意干净环境（受限网络 Linux 云端容器或 Windows/macOS 本地）从 GitHub 私有仓库独立恢复 Rei Desktop Pet 工程并复验全部核心资产与三套标准图集。

> **跨平台复算已实证通过**：本仓库已于 **Windows 本地（Python 3.14.6 / Pillow 12.3.0）** 与 **Antigravity Cloud Linux 容器（Ubuntu 24.04.5 LTS / Python 3.12.16 / Pillow 13.0.0 / libwebp 1.6.0 / zlib 1.3）** 双端独立完成全量恢复复算，三套重装标准 PNG 图集不仅解码 RGBA 像素 100% 一致，**文件 SHA-256 亦 100% 逐字节一致**（详见 [CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md) 与 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)）。

---

## 1. 干净恢复步骤

### 1.1 受限网络 Linux 云端容器（无 PyPI，使用容器预装 Pillow）

```bash
git clone https://github.com/waynewayne893/rei-desktop-pet.git
cd rei-desktop-pet
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
# 验证预装 Pillow 与 libwebp 版本（实测基线：Pillow 13.0.0, libwebp 1.6.0, zlib 1.3）
python3 -c "import PIL, PIL.features as f; print(PIL.__version__, f.version('webp'))"
```

### 1.2 有网络权限的本地环境（Windows / macOS / Linux）

```bash
git clone https://github.com/waynewayne893/rei-desktop-pet.git
cd rei-desktop-pet
python3 -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 2. 一键完整性核验（冻结母版 + 派生母版 + 171 帧 + 三套标准图集）

推荐使用零外置依赖（仅 Python 标准库 + Pillow）工具执行全量核验：

```bash
python3 06_共用工具/rei_compat_builder.py verify
```

预期返回退出码 `0` 且 JSON 输出 `"ok": true`、`"verified_frozen_and_backups": 6`、`"verified_derived_masters": 3`、`"verified_frames": 171`、`"verified_atlases": 3`，同时逐一核对：
- `00_原始美术母版/` 三套冻结原画及 `P2_字节备份/` SHA-256；
- `02_标准化母版/` 三套 P3 / P3-FIX 派生母版 SHA-256；
- `07_QA验收/REI_P4B_ASSET_MANIFEST.json` 登记的全部 171 帧 PNG 哈希、尺寸 (`192×208 RGBA`)、1px 边框透明留白、零隐藏 RGB 与单一 8 连通主体；
- 三套 `delivery/spritesheet-standard.png` 哈希、零透明 RGB 残留及 57 有效格 / 15 空格结构。

---

## 3. 独立重新装配三套标准图集并逐像素 / SHA-256 对拍

```bash
python3 06_共用工具/rei_compat_builder.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets
```

该命令从 171 个独立注册帧重新拼装三套 `1536×1872 RGBA` 标准图集，执行独立结构校验，并与仓库内提交的 `*/P4-B/delivery/spritesheet-standard.png` 逐像素比对（`pixel_identical_to_committed: true`）并核对 SHA-256（Linux/Windows 实测均为 `sha256_identical: true`）。

### 关键基线哈希真值

| 资产 | 仓库相对路径 | SHA-256 |
| --- | --- | --- |
| 校服冻结母版 | `00_原始美术母版/rei-school-base-v1.0.png` | `68d79674728e46b1bbff62070b9e57c79ad6e3b9f70354a344539b26511b0bc1` |
| 白服冻结母版 | `00_原始美术母版/rei-white-base-v1.0.png` | `ec683e7185e0399494a1f5be1ff6de74f7187c22999bc72b7daded626b179019` |
| 黑服冻结母版 | `00_原始美术母版/rei-black-base-v1.0.png` | `be5907538ecbade28ed82ba8236c5fd461b119f5ef928a1289d7488429aed7cb` |
| 校服标准图集 | `03_校服绫波丽/P4-B/delivery/spritesheet-standard.png` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` |
| 白服标准图集 | `04_白色战斗服/P4-B/delivery/spritesheet-standard.png` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` |
| 黑服标准图集 | `05_黑色战斗服/P4-B/delivery/spritesheet-standard.png` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` |
| P4-COMPAT 测试包 v2 图集（临时） | `07_QA验收/P4-COMPAT/rei-compat-test/spritesheet.webp` | `bd6d29f401738015dddf452a79ffc460e6d53851f1ce691cbf25dd4605365201` |

---

## 4. Windows 原生平台门禁与历史脚本说明

- **最终平台门禁**：在已安装 `OpenAI.Codex`（已验证版本 `26.1120.6357.0`）的 Windows 本机，只读调用其内置 `hatch-pet\scripts\validate_atlas.py --require-v2` 做最终平台双校验（`P4-COMPAT` 预验证已实测退出码 `0`、0 错误、0 警告，见 [WINDOWS_NATIVE_VALIDATION_V2.json](07_QA验收/P4-COMPAT/WINDOWS_NATIVE_VALIDATION_V2.json)）。
- **历史脚本留档**：以下 5 个历史 Windows 脚本按原字节留档以保留完整审计链：`02_标准化母版/build_static_masters.py`、`02_标准化母版/P3-FIX/build_p3_fix.py`、`07_QA验收/P4-A/build_preview_row.py`、`07_QA验收/P4-B/build_rows.py`、`07_QA验收/P4-B/assemble_delivery.py`。
