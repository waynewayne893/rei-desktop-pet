# REI-PET-P4C-PRODUCTION｜方向帧候选与 QA

2026-11-27 · 统一基准 `6b4229f76d44caf234c3120d65a71bd59989e647` · 独立分支 `feat/p4c-production`

**48/48 方向帧 `STRUCTURE_PASS`。** 黑服 000°、090°、180°、270° 继承已绑定的人工 `ACCEPTED`，新生成 44 帧为 `PENDING_HUMAN_REVIEW`。原有 27 动作、171 帧继续为 `ACCEPTED`，新版校服 waiting 仍是已通过的备用候选。

## 生产与证据

| 形态 | 复用 | 新生成候选 | 生成批次 `STRUCTURE_PASS` / `FAILED` | 实体高度 | 实测脚底 X / Y |
| --- | ---: | ---: | ---: | --- | --- |
| 校服 | 0 | 16 | 5 / 0 | 186–189 px | 95.5–96.5 / 194–195 |
| 白服 00 | 0 | 16 | 7 / 3 | 186–188 px | 95.5–96.5 / 194–195 |
| 黑服 09 | 4 | 12 | 4 / 2 | 186–190 px | 95–96.5 / 194–196 |

每批保留生图工具直接返回的原始 PNG、提示词、技术结果和选用记录。21 批原图与提示词的 SHA-256 已重新计算。逐批复算确认，原始 Alpha 清理只将恰好等于 1/255 的像素置零，记录了准确数量、处理前后 RGBA 像素哈希及原始 PNG 文件哈希。任何原图边缘 Alpha 高于 1/255 的批次仍判失败。拆分后以 188 px 和 (96,195) 为基准，同批次共用等比缩放、逐格平移登记。人物姿态和方向来自原生生成。

四张黑服复用 PNG 逐字节等于 attempt-02，原始生成图、派生母版、候选版本及四项人工决定的哈希均核验。原始失败 attempt-01 保留在专项试验档案。 [正式方向资产清单](P4C_DIRECTION_ASSET_MANIFEST.json) · [复用登记](rei-black/reuse.json)

## 结构、边缘与方向阅读

- 每格为 192×208 RGBA PNG，透明边框完整，Alpha=0 处 RGB 全零，Alpha≥128 的实心前景各为单一 8 连通分量。每套 16 帧像素均不同，左右对应帧无精确镜像相等。登记帧的低 Alpha 独立分量最大 15 px、峰值 Alpha 4/255，已逐帧记录并用明暗底对照。
- 按冻结顺序检查每套 16 帧，包括 157.5°→180° 与 337.5°→000°。校服交握手和白发夹、白服 00 与垂臂、黑服 09 与右手扶左臂的特征可辨。方向间距的主观均匀性仍留给人工审阅，重点对照校服 090°→112.5°、180°→202.5°，白服近水平及近 12 点过渡，以及黑服 022.5°、202.5° 的轻微侧偏。
- 独立评审只看到打乱顺序的局部图。首轮 11/12 个方向可辨，白服首轮 000° 读向不清。重做后白服复检 4/4，目前采用的四基准方向共 12/12 可辨。黑服 000° 和白服左右转头的幅度较轻。盲检为机器辅助验证，44 张新帧仍待人工。 [盲检记录](P4C_CARDINAL_BLIND_TEST.json) · [结构 QA 明细](P4C_STRUCTURE_QA.json) · [独立复算统计](P4C_ASSET_AUDIT_SUMMARY.json)

| 形态 | 16 方向接触表 | 顺时针预览 |
| --- | --- | --- |
| 校服 | [浅底](rei-school/review/contact-light.png) · [深底](rei-school/review/contact-dark.png) | [浅底 GIF](rei-school/review/clockwise-light.gif) · [深底 GIF](rei-school/review/clockwise-dark.gif) |
| 白服 | [浅底](rei-white/review/contact-light.png) · [深底](rei-white/review/contact-dark.png) | [浅底 GIF](rei-white/review/clockwise-light.gif) · [深底 GIF](rei-white/review/clockwise-dark.gif) |
| 黑服 | [浅底](rei-black/review/contact-light.png) · [深底](rei-black/review/contact-dark.png) | [浅底 GIF](rei-black/review/clockwise-light.gif) · [深底 GIF](rei-black/review/clockwise-dark.gif) |

## Review Center 离线复验

仓库版和独立解压版各运行方向测试与原有回归测试，共四次浏览器检查通过。每版均核验 48 张方向帧实际 PNG SHA-256 和 192×208 显示尺寸、方向选择和绕回、底色切换、独立方向 JSON 导入导出、哈希失效和复用状态锁定。正式 27 条动作、171 帧与专项 10 帧的状态和交互回归通过。浏览器错误、失败与外部请求均为 0。

平台管理的 Chromium 限制 `file://`。解压版通过本机回环验证。离线包包含 268 项，ZIP SHA-256 为 `2877a8f49c46c75a051dadd32b7d837b1dcde2c6255b37227fe7d4c1453a62cf`。 [离线 Review Center](../Review-Center/rei-review-center-v1.0-offline.zip)

## 停止边界

统一基准的冻结原画及备份、三套派生母版、171 张正式帧、三套标准图集和原有验收原件保持原字节。P4-C 候选与证据位于独立本地任务分支，等待推送及人工终审授权。P4-D 扩展图集装配、安装与发布留待后续阶段。
