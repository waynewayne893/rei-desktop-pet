# P4D_PACKAGE_INTEGRITY_FIX_REPORT.md｜P4-D 交付包循环哈希依赖修复报告

- **任务代号**：`REI-PET-P4D-INTEGRITY-FIX`
- **主控前置裁定**：`P4-D_PACKAGE_INTEGRITY_FIX_REQUIRED` / `P5_INSTALLATION_BLOCKED`
- **基线来源**：`feat/p4d-final-assembly`（Commit `6561fbde2605e81fd1077701bd681ab438135441`）
- **独立修复分支**：`fix/p4d-package-integrity`
- **修复状态**：**`INTEGRITY_FIX_VERIFIED_PASS`（10/10 独立完整性测试全部通过；所有上游与 P4-D 受保护美术/安装包资产与 `6561fbd` 逐字节一致）**

---

## 1. 缺陷根因（`6561fbd`）

在 `6561fbde2605e81fd1077701bd681ab438135441` 的 `06_共用工具/p4d_assemble.py`（原 `finalize_bundle_and_sums` 第 722–814 行）中存在两处循环哈希依赖：

1. **外层清单与外层校验和互相引用**：原逻辑先将旧版 `SHA256SUMS.txt` 哈希写入 `P4D_DELIVERY_MANIFEST.json["sha256sums_file"]`，随后又把更新后的 `P4D_DELIVERY_MANIFEST.json` 与总 ZIP 写入新的 `SHA256SUMS.txt`，导致外层 Manifest 内记录的 `SHA256SUMS.txt` 哈希永远过时。
2. **外层清单打入自身校验的总 ZIP**：原逻辑把 `P4D_DELIVERY_MANIFEST.json` 与 `SHA256SUMS.txt` 打包进 `rei-desktop-pet-p4d-all-3-bundle.zip`，随后再把新总 ZIP 哈希回写至外层 `P4D_DELIVERY_MANIFEST.json`，导致总 ZIP 内部携带的是上一版总 ZIP 的过期哈希。

---

## 2. 修复设计：单向无环内外双层完整性架构（Acyclic Two-Layer DAG）

已重构 [p4d_assemble.py](../../06_共用工具/p4d_assemble.py) 的 `finalize_bundle_and_sums`，严格按以下**单向拓扑顺序一次生成**（零重打包、零自引用、零循环依赖），并新增独立校验入口 `--verify-integrity`：

```text
21 个不可变交付载荷文件（与 6561fbd 逐字节一致）
  └──> [内层] PAYLOAD_MANIFEST.json（仅记录 21 个载荷资产；不记录总 ZIP、任何 SUMS 或自身）
         └──> [内层] PAYLOAD_SHA256SUMS.txt（ZIP 内相对路径校验 21 载荷 + PAYLOAD_MANIFEST.json = 22 条；不含自身）
                └──> rei-desktop-pet-p4d-all-3-bundle.zip（单次确定性打包 21 载荷 + 内层 Manifest + 内层 SUMS = 23 项；严禁打入外层文件）
                       └──> [外层] P4D_DELIVERY_MANIFEST.json（记录交付资产 + 内层双清单 + 最终总 ZIP 哈希；严禁记录外层 SHA256SUMS.txt）
                              └──> [外层终节点] SHA256SUMS.txt（校验全部外层交付物 + 内层双清单 + 最终总 ZIP + 外层 Manifest = 31 条；不含自身）
```

---

## 3. 更新后的总交付 ZIP 与双层清单哈希

| 文件（仓库相对路径） | 层级 | 体积 (Bytes) | SHA-256 |
| --- | :---: | ---: | --- |
| `08_正式交付/P4-D-candidate/PAYLOAD_MANIFEST.json` | 内层 | `5,930` | `8103d2c66d08aaf152fd5f8f765d4b4e60a101a6004736f54e16547e06f9552d` |
| `08_正式交付/P4-D-candidate/PAYLOAD_SHA256SUMS.txt` | 内层 | `2,329` | `c29d32c87cf6f39c539f7f6af6825e44b883540017e1015b8f9398b43cc61559` |
| `08_正式交付/P4-D-candidate/rei-desktop-pet-p4d-all-3-bundle.zip` | 总包（23 项） | `17,041,033` | `c0fe9485ffa2720ff9fdfd64e3c6b41f34a8a5769a85814bc74fb7b627ccbdc7` |
| `08_正式交付/P4-D-candidate/P4D_DELIVERY_MANIFEST.json` | 外层 | `120,858` | `a933a31772f215de1f93614314773aab6e5ac9c09f37d2c8d4048c10daa47fe6` |
| `08_正式交付/P4-D-candidate/SHA256SUMS.txt` | 外层终节点（31 条） | `3,793` | `9fde179ce8984d870975ae334520ff9bc3627defa37607debe0c0fbf2c7bd5f6` |

---

## 4. 10 项独立完整性测试实测结果（全部 PASS）

结构化证据详见 [P4D_PACKAGE_INTEGRITY_TEST.json](P4D_PACKAGE_INTEGRITY_TEST.json)：

| # | 测试项 | 结果 | 实测指标 |
| ---: | --- | :---: | --- |
| 1 | 外部 `P4D_DELIVERY_MANIFEST.json` 全部哈希核验 | **PASS** | `302 / 302` 条引用哈希全部匹配 |
| 2 | 外部 `SHA256SUMS.txt` 全部条目核验 | **PASS** | `31 / 31` 条全部匹配 |
| 3 | 总 ZIP 解压与 CRC 检查（`testzip() is None`） | **PASS** | `23` 项全部完整无损 |
| 4 | 内部 `PAYLOAD_MANIFEST.json` 全部哈希核验（解压副本） | **PASS** | `21 / 21` 载荷文件全部匹配 |
| 5 | 内部 `PAYLOAD_SHA256SUMS.txt` 全部条目核验（解压副本） | **PASS** | `22 / 22` 条（ZIP 相对路径）全部匹配 |
| 6 | 内外相同交付文件逐字节比较 | **PASS** | `23 / 23` 文件逐字节 100% 一致 |
| 7 | 连续两次 `--bundle-only` 打包幂等性验证 | **PASS** | Run 1 与 Run 2 全部 5 个生成物 SHA-256 逐字符一致 |
| 8 | 独立临时副本单字节损坏检测（外层 + 内层双测） | **PASS** | 翻转外层 `rei-school/pet.json` 1 字节被拒绝；翻转解压内层 `pets/rei-black/spritesheet.webp` 1 字节被内层 Manifest 与内层 SUMS 双重拒绝 |
| 9 | 无环 DAG 与非自引用不变量检查 | **PASS** | `12 / 12` 项不变量全部通过（无 `sha256sums_file` 键、总 ZIP 无外层文件、各清单与校验和均无自引用/循环引用） |
| 10 | 上游与 P4-D 受保护资产与 `6561fbd` 逐字节对比 | **PASS** | 6 冻结与备份、3 派生母版、171 标准帧、48 方向帧（合计 219 帧）、3 标准图集、3 扩展 PNG、6 WebP 副本、6 `pet.json`、3 套独立安装 ZIP、6 接触表及既有 QA/P5 文档 **0 字节改动** |

---

## 5. 停止边界确认

- 本次修复**未重新编码任何 WebP、未重新装配任何图集、未调用生图工具**；
- 仅改动 `06_共用工具/p4d_assemble.py` 与 `08_正式交付/P4-D-candidate/` 下的双层校验清单及总交付 ZIP，并新增本修复报告与测试 JSON；
- 未安装任何宠物、未触碰 Asuka、未修改 `main`、未发布 `v1.0.0`；
- 推送 `fix/p4d-package-integrity` 后停止，等待 ChatGPT 主控独立验收后由 Codex 恢复 P5。
