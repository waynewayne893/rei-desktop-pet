# REI-PET-P4B → P4C｜交接至 16 方向注视阶段

**当前阶段：P4-B `PARTIAL_PENDING_ART_REVIEW`。P4-C 尚未授权启动。**

本轮由 Google Antigravity 接管完成 P4-B 断点审计、全部 21 条新增候选的视觉与标识复核、三套标准 `1536×1872` 图集装配（每套 57 有效格 + 15 全透明空格，合计 171 帧）、`validate_atlas.py` 结构校验、明暗底总接触表与 18 个三形态同步 GIF 交付。

---

## 1. P4-B 已就绪的下游输入（经哈希锁定）

待用户与主控签收 P4-B 美术后，以下三套标准图集可作为 P4-D 扩展装配（`1536×2288`，57 标准动作 + 16 方向注视 + `(0,6)` 中性格 = 74 有效格 + 14 空格）的前九行输入：

| 形态 | 标准图集路径 | SHA-256 | 校验状态 |
| --- | --- | --- | --- |
| `rei-school` | `03_校服绫波丽/P4-B/delivery/spritesheet-standard.png` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` | `STRUCTURE_PASS` |
| `rei-white` | `04_白色战斗服/P4-B/delivery/spritesheet-standard.png` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` | `STRUCTURE_PASS` |
| `rei-black` | `05_黑色战斗服/P4-B/delivery/spritesheet-standard.png` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` | `STRUCTURE_PASS` |

---

## 2. 进入 P4-C 的必须前置条件

1. **用户与 ChatGPT 主控完成 P4-B 人工美术验收**：
   - 审阅三套明/暗底 9 行总接触表与 9 状态明/暗底同步对比 GIF；
   - 确认是否接受以下轻微循环过渡观察项，或指定其中任意单条做局部修复：
     - `rei-school / waiting`（F6 举掌→F1 交握循环切回）
     - `rei-black / review`（F5–F6 垂臂→F1 扶臂循环切回）
     - `rei-black / waving`（F1/F4 双臂放松垂放）
2. **Antigravity 图像生成最小实测门禁（P4-C 首步必做）**：
   - 因 P4-B 21 条动作已由 Codex 完整生成且无阻断缺陷，Antigravity 本轮未实测图像生成；
   - P4-C 的 16 方向注视（行 9：000°–157.5°，行 10：180°–337.5°）需要**新图像生成**；
   - 获准启动 P4-C 后，第一步必须先以单一形态的 4 基准方向（000°、090°、180°、270°）做最小真实候选测试，验证：参考冻结/派生母版的角色一致性、原生 RGBA 真透明（或确认透明抠图需求与合规门禁）、与 `hatch-pet` 提取/注册链路的兼容性；实测通过后再扩大至全部 16 方向 × 3 形态。
3. **继续严守隔离与红线**：
   - 不得修改 `00_原始美术母版/`、`02_标准化母版/`、明日香参考工程 `D:\HuaweiMoveData\Users\86191\Desktop\Codex_Asuka` 及 `C:\Users\86191\.codex\pets` 下已有宠物；
   - P4-C 仅生产 16 方向注视并通过四基准盲检与跨行连续性检查，不提前跳步至 P4-D 扩展装配、P5 注册或 P6 推送。

---

## 3. 索引

- [接管审计与执行报告](../07_QA验收/AGY_TAKEOVER_REPORT.md)
- [P4-B 离线 QA 报告](../07_QA验收/REI_P4B_QA_REPORT.md)
- [3×9 动作恢复矩阵](../07_QA验收/REI_P4B_RESUME_MATRIX.json)
- [工具链能力清单](../07_QA验收/AGY_TOOLCHAIN_CAPABILITY.json)
- [P4-B 完整资产清单](../07_QA验收/REI_P4B_ASSET_MANIFEST.json)
- [前后保护哈希证据](../07_QA验收/P4-B/agy-preservation-hashes.json)
