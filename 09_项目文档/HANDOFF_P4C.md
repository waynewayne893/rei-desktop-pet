# REI-PET-P4B → P4C｜交接至 16 方向注视阶段

**当前阶段：`P4-B_ART_ACCEPTANCE_PASS`、`P4-C_PRODUCTION_AUTHORIZED`。**

本轮由 Google Antigravity 接管完成 P4-B 断点审计、全部 21 条新增候选的视觉与标识复核、三套标准 `1536×1872` 图集装配（每套 57 有效格 + 15 全透明空格，合计 171 帧）、`validate_atlas.py` 结构校验、明暗底总接触表与 18 个三形态同步 GIF 交付。

---

## 1. P4-B 已就绪的下游输入（经哈希锁定）

P4-B 美术已签收。以下三套标准图集可作为 P4-D 扩展装配（`1536×2288`，57 标准动作 + 16 方向注视 + `(0,6)` 中性格 = 74 有效格 + 14 空格）的前九行输入：

| 形态 | 标准图集路径 | SHA-256 | 校验状态 |
| --- | --- | --- | --- |
| `rei-school` | `03_校服绫波丽/P4-B/delivery/spritesheet-standard.png` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` | `STRUCTURE_PASS` |
| `rei-white` | `04_白色战斗服/P4-B/delivery/spritesheet-standard.png` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` | `STRUCTURE_PASS` |
| `rei-black` | `05_黑色战斗服/P4-B/delivery/spritesheet-standard.png` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` | `STRUCTURE_PASS` |

---

## 2. P4-C 接续门禁

1. 两份人工验收原件及资产绑定已归档。校服新版 waiting 为已通过备用候选，标准图集继续使用原版。 [验收台账](../07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json)
2. 基准统一后单独建 P4-C 分支。先将已验证的黑服 attempt-02 000°、090°、180°、270° 登记，再按每套先四基准方向、后过渡方向的顺序生成剩余 44 帧。
3. 保留冻结母版、原有 171 帧、Asuka 工程及安装资产。P4-C 在 48 帧离线 QA 和人工终审入口处收口，P4-D 扩展图集另行授权。

---

## 3. 索引

- [接管审计与执行报告](../07_QA验收/AGY_TAKEOVER_REPORT.md)
- [P4-B 离线 QA 报告](../07_QA验收/REI_P4B_QA_REPORT.md)
- [3×9 动作恢复矩阵](../07_QA验收/REI_P4B_RESUME_MATRIX.json)
- [工具链能力清单](../07_QA验收/AGY_TOOLCHAIN_CAPABILITY.json)
- [P4-B 完整资产清单](../07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- [前后保护哈希证据](../07_QA验收/P4-B/agy-preservation-hashes.json)
