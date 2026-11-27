# REPRODUCIBILITY.md｜独立环境恢复与复算指南

本指南说明如何在任意干净环境（Linux 云端或 Windows 本地）从 GitHub 私有仓库独立恢复 Rei Desktop Pet 工程并复验全部核心资产与三套标准图集。

---

## 1. 干净恢复步骤

```bash
# 1. 克隆唯一官方私有仓库
git clone https://github.com/waynewayne893/rei-desktop-pet.git
cd rei-desktop-pet

# 2. 创建隔离 Python 环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 2. 一键完整性核验（冻结母版 + 派生母版 + 171 帧 + 三套标准图集）

```bash
python3 06_共用工具/rei_atlas_tools.py verify
```

预期返回退出码 `0` 且 JSON 输出 `"ok": true`、`"verified_frames": 171`、`"verified_atlases": 3`，同时逐一核对：
- `00_原始美术母版/` 三套冻结原画及 `P2_字节备份/` SHA-256；
- `02_标准化母版/` 三套 P3 / P3-FIX 派生母版 SHA-256；
- `07_QA验收/REI_P4B_ASSET_MANIFEST.json` 登记的全部 171 帧 PNG 哈希、尺寸 (`192×208 RGBA`)、边框透明留白、零隐藏 RGB 与单一 8 连通主体；
- 三套 `delivery/spritesheet-standard.png` 哈希及 57 有效格 / 15 空格结构。

---

## 3. 独立重新装配三套标准图集并逐像素对拍

```bash
python3 06_共用工具/rei_atlas_tools.py reassemble --out-dir /tmp/rei-reassemble-check --write-sheets
```

该命令将从 171 个独立注册帧重新拼装三套 `1536×1872 RGBA` 标准图集，执行独立结构校验，并与仓库内提交的 `*/P4-B/delivery/spritesheet-standard.png` 逐像素比对（`pixel_identical_to_committed: true`）并核对 SHA-256。

### 关键基线哈希真值

| 资产 | 仓库相对路径 | SHA-256 |
| --- | --- | --- |
| 校服冻结母版 | `00_原始美术母版/rei-school-base-v1.0.png` | `68d79674728e46b1bbff62070b9e57c79ad6e3b9f70354a344539b26511b0bc1` |
| 白服冻结母版 | `00_原始美术母版/rei-white-base-v1.0.png` | `ec683e7185e0399494a1f5be1ff6de74f7187c22999bc72b7daded626b179019` |
| 黑服冻结母版 | `00_原始美术母版/rei-black-base-v1.0.png` | `be5907538ecbade28ed82ba8236c5fd461b119f5ef928a1289d7488429aed7cb` |
| 校服标准图集 | `03_校服绫波丽/P4-B/delivery/spritesheet-standard.png` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` |
| 白服标准图集 | `04_白色战斗服/P4-B/delivery/spritesheet-standard.png` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` |
| 黑服标准图集 | `05_黑色战斗服/P4-B/delivery/spritesheet-standard.png` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` |

---

## 4. 历史 Windows 脚本复算说明

以下 5 个历史脚本按原字节留档以保留完整审计链，不建议直接修改原件：
- `02_标准化母版/build_static_masters.py`（依赖 Windows 字体 `C:/Windows/Fonts/consola.ttf`）
- `02_标准化母版/P3-FIX/build_p3_fix.py`（依赖 Windows 字体）
- `07_QA验收/P4-A/build_preview_row.py`（依赖 `--hatch-scripts` 与 Windows 字体）
- `07_QA验收/P4-B/build_rows.py`（依赖 `hatch-pet/scripts` 路径参数）
- `07_QA验收/P4-B/assemble_delivery.py`（依赖 `hatch-pet/scripts` 路径参数与 Windows 字体）

在 Windows 本机且已安装 `OpenAI.Codex 26.1120.6357.0` 时，可继续以只读方式传入其 `hatch-pet/scripts` 目录运行官方 `validate_atlas.py` 双校验；在 Linux 云端环境，统一通过 `06_共用工具/rei_atlas_tools.py` 实现同等确定性校验与装配。
