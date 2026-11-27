# REI-PET-P4-B｜三套标准 9 行动作离线 QA 报告

**建议裁定：`PARTIAL_PENDING_ART_REVIEW`（三套 57 帧标准图集结构校验全部 `STRUCTURE_PASS`，171/171 帧视觉与标识离线预检通过，待用户与 ChatGPT 主控人工动态美术验收）。**

---

## 1. 标准图集结构校验汇总

三套图集均由 `07_QA验收/P4-B/assemble_delivery.py` 调用 `hatch-pet/scripts/compose_atlas.py` 装配，并由 `hatch-pet/scripts/validate_atlas.py` 独立复核（退出码均为 `0`，错误与警告均为 `0`）：

| 形态 | 图集尺寸 / 模式 | 有效格 / 全透明格 | 校验文件 | 亮底 9 行接触表 | 深底 9 行接触表 |
| --- | --- | :---: | --- | --- | --- |
| `rei-school` | 1536×1872 RGBA | 57 / 15 | [validation.json](../03_校服绫波丽/P4-B/delivery/spritesheet-standard-validation.json) | [亮底总表](../03_校服绫波丽/P4-B/delivery/standard-contact-sheet.png) | [深底总表](../03_校服绫波丽/P4-B/delivery/standard-contact-sheet-dark.png) |
| `rei-white` | 1536×1872 RGBA | 57 / 15 | [validation.json](../04_白色战斗服/P4-B/delivery/spritesheet-standard-validation.json) | [亮底总表](../04_白色战斗服/P4-B/delivery/standard-contact-sheet.png) | [深底总表](../04_白色战斗服/P4-B/delivery/standard-contact-sheet-dark.png) |
| `rei-black` | 1536×1872 RGBA | 57 / 15 | [validation.json](../05_黑色战斗服/P4-B/delivery/spritesheet-standard-validation.json) | [亮底总表](../05_黑色战斗服/P4-B/delivery/standard-contact-sheet.png) | [深底总表](../05_黑色战斗服/P4-B/delivery/standard-contact-sheet-dark.png) |

---

## 2. 逐帧像素级结构门禁（171 帧全检）

- **单帧规格**：171/171 帧均解码为 `192×208 RGBA`，等比缩放注册，锚点统一为 `(96, 195)`，无非等比拉伸。
- **Alpha 卫生**：171/171 帧四边至少留白 `>= 4 px`（最小顶边距 `4 px` 出现在 `jumping`/`failed`/`running-left` 动态高点，无任何裁切），透明区残留非零 RGB 像素数为 `0`，`Alpha>=128` 均为单一 8 连通主体，每行帧间像素互不重复。
- **图集一致性**：`assemble_delivery.py` 对三套 `spritesheet-standard.png` 的全部 72 个格位做了逐字节回读比对——57 个有效格逐字节等于对应注册帧，15 个空格逐字节全零透明。

---

## 3. 逐动作离线美术与标识审查（9 状态 × 3 形态）

高分辨率胸前标识实图核验见：[白服 00 标识拼图](P4-B/p4b-chest-markings-qa-white.png) · [黑服 09 标识拼图](P4-B/p4b-chest-markings-qa-black.png)。

| 行 | 状态 | 帧数 | 三形态对比 GIF | 离线美术、标识、语义与连续性检查结论 |
| ---: | --- | ---: | --- | --- |
| 0 | `idle` | 6 | [亮底](P4-B/comparison-gifs/idle-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/idle-three-form-dark.gif) | 沿用 P4-A 受保护基线（白服为修复后的 `attempt-02`）。校服交握、白服垂臂、黑服右扶左臂，眨眼与微呼吸平稳。 |
| 1 | `running-right` | 8 | [亮底](P4-B/comparison-gifs/running-right-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/running-right-three-form-dark.gif) | 沿用 P4-A 受保护基线，其中黑服为**用户已明确验收的 FIX-BLACK 新版**（旧版 `REJECTED` 已排除）。三套均自然摆臂、交替步态。 |
| 2 | `running-left` | 8 | [亮底](P4-B/comparison-gifs/running-left-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/running-left-three-form-dark.gif) | 三套均独立生成向左跑动（非简单水平镜像）。高分原图复核：**白服 `00` 与黑服红色 `09` 全部正向清晰、无镜像畸变**。黑服解除固定扶臂并自然摆臂，三套均无裁切（最小顶余量 4–6 px）。 |
| 3 | `waving` | 4 | [亮底](P4-B/comparison-gifs/waving-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/waving-three-form-dark.gif) | 三套均有明显右手抬起挥手动作（F2–F3）并回落（F4），五指轮廓与 `00`/`09` 完整。提示人工复核：黑服 F1/F4 为双臂放松垂放（动态未锁定扶臂）。 |
| 4 | `jumping` | 5 | [亮底](P4-B/comparison-gifs/jumping-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/jumping-three-form-dark.gif) | 三套均完整呈现下蹲蓄力(F1)→起跳(F2)→腾空高点(F3，脚底抬离基准 12–17 px)→落地缓冲(F4)→站立回正(F5)。顶部无裁切（最小顶余量 4 px）。 |
| 5 | `failed` | 8 | [亮底](P4-B/comparison-gifs/failed-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/failed-three-form-dark.gif) | 三套均表现失落、垂眸与短暂低头（F3–F5/F6）后缓回，语义贴合绫波丽性格。校服保持交握，黑服保持右扶左臂，白服轻握微低头，首尾顺畅。 |
| 6 | `waiting` | 6 | [亮底](P4-B/comparison-gifs/waiting-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/waiting-three-form-dark.gif) | 表达等待输入/授权：歪头注视并轻抬摊手示意。白服与黑服 F4–F6 收手闭眼再睁眼，循环平顺；**提请人工关注**：校服 F3–F6 持续保持左手轻抬，F6→F1 回交握手时姿态切换较直接。 |
| 7 | `running` | 6 | [亮底](P4-B/comparison-gifs/running-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/running-three-form-dark.gif) | 准确表达「Codex 工作中/凝神思考」而非横向跑步：三套均在 F2–F6 抬手至下颌/胸前并伴随视线专注与 F4 眨眼，与 `running-left/right` 语义区分清晰。 |
| 8 | `review` | 6 | [亮底](P4-B/comparison-gifs/review-three-form-light.gif) · [深底](P4-B/comparison-gifs-dark/review-three-form-dark.gif) | 表达查看、审阅与点头确认：F1–F2 凝视→F3 前倾察看→F4 闭眼确认→F5 抬头回正→F6 复位。**提请人工关注**：黑服 F1–F4 扶臂、F5–F6 垂臂，循环回 F1 时由垂臂切回扶臂。 |

---

## 4. 深浅背景与边缘视觉核验

- **浅底 (`#f0f3f9`)**：三套轮廓、发梢、白袖白袜、白服高光及黑服腿部步态均清晰无白边或杂色溢出。
- **深底 (`#263242`)**：校服与白服轮廓锐利、无灰白发光边；黑服暗色裤腿与深底对比度偏低属原画深色配色固有表现，浅蓝发丝、红绿胸饰与红靴缘保持清晰辨识。

---

## 5. 逐状态审阅拼图与清单索引

- 7 状态单行审阅拼图：[running-left](P4-B/review-running-left-attempt-01.png) · [waving](P4-B/review-waving-attempt-01.png) · [jumping](P4-B/review-jumping-attempt-01.png) · [failed](P4-B/review-failed-attempt-01.png) · [waiting](P4-B/review-waiting-attempt-01.png) · [running](P4-B/review-running-attempt-01.png) · [review（Antigravity 补齐）](P4-B/review-review-attempt-01.png)
- 完整清单与证据：[REI_P4B_ASSET_MANIFEST.json](REI_P4B_ASSET_MANIFEST.json) · [visual-selection.json](P4-B/visual-selection.json) · [agy-preservation-hashes.json](P4-B/agy-preservation-hashes.json)

---

## 6. 门禁检查项

- [√] 3×9 全部 27 条动作（171 帧）齐全、原生透明、零裁切、零隐藏 RGB
- [√] 三套 `1536×1872` 标准图集装配完成并通过 `validate_atlas.py`（57 有效格 + 15 空格，0 error / 0 warning）
- [√] 白服 `00` 与黑服 `09` 高分辨率正向核验通过；旧黑服 `running-right` 明确排除
- [√] 冻结母版、P3/P3-FIX、P4-A 42 帧、明日香工程与已安装宠物哈希前后一致
- [ ] 用户与 ChatGPT 主控人工动态美术验收（通过后方可授权 P4-C）
