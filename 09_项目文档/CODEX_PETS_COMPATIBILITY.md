# Codex Pets 兼容性审计

**范围** Windows 桌面版 `OpenAI.Codex 26.1120.6357.0`。安装根 `C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0`。在其 `app/resources/skills/skills/.curated/hatch-pet/` 读取 `SKILL.md`、`references/codex-pet-contract.md`、`references/animation-rows.md` 和实际脚本。在同版本 `app/resources/app.asar` 只读查找播放、注册与状态分发代码。

| 基线项目 | 当前证据及裁定 |
| --- | --- |
| 192×208 单格 | 随附规范、播放布局常量和旧图格实测一致 |
| 标准 8×9、57 帧 | 1536×1872，15 空格。随附工具实跑两张均通过。新宠物以此作中间图 |
| 扩展 8×11、1536×2288 | 安装版读取与渲染定义、工具和历史安装资产一致 |
| 16 个方向帧 | 顺时针数组和指针扇区逻辑一致 |
| 73 格 | 安装版渲染表使用这 73 个动作与方向格，旧包实测吻合。当前打包校验另要求 `(0,6)` 中性注视格，最终打包规划 74 个有内容格、14 个全透明格 |
| WebP | 现有包全部是有 Alpha 的单帧 WebP。规范及加载源码允许 PNG 或 WebP，项目交付沿用 `spritesheet.webp` |

## 版本分歧

- 2026-10-26 的 Asuka 历史服务预检按 `[6,8,8,4,5,8,6,6,6,8,8]` 返回通过，编码哈希与现有两套安装包一致。Work Pets 插件 `work-pets/0.1.6` 的规范同样描述 73 个有效格，当前实跑其 `validate_atlas.py --require-v2` 校服安装 WebP 通过。
- 当前桌面随附的 `scripts/assemble_extended_atlas.py` 提供 `--neutral-cell`，通过 `paste_neutral_cell` 写到第 0 行第 6 列，并在装配元数据记录 `neutralLookFrame`。`scripts/validate_atlas.py` 的 `EXTENDED_NEUTRAL_LOOK_FRAME = (0, 6)` 将该格加入 v2 的使用格。实跑 12 个 Asuka 扩展副本均只因这格透明而失败，详情见 [复跑证据](../07_QA验收/ASUKA_P2_READONLY_EVIDENCE.json)。
- 同版本应用播放器主表的 `requiredFramesByRow` 仍为 73，并将 idle 播放限制在列 0–5。应用另有正面中心死区回退逻辑。尚无现场证据证明浮窗会显示辅助中性格。桌面候选采用随附装配器的中性格；最终编码的真实校验和加载由 P5 验证。

## 九状态及注视映射

行列均从 0 开始；每个标准动作按列从左到右取帧。时间来自随附 `animation-rows.md`，并与应用播放代码的基础动作表吻合。右栏注明触发的证据级别。

| 行 | 状态 | 占用列 | 基础毫秒 | 触发与证据 |
| ---: | --- | --- | --- | --- |
| 0 | `idle` | 0–5 | 280, 110, 110, 140, 140, 320 | 活动状态回退与安静待机；减少动态效果路径可取当前状态首格。列 6 供扩展装配 |
| 1 | `running-right` | 0–7 | 120×7 + 220 | 浮窗无轨道物理的拖动分支中，横移向右达到 4 个屏幕坐标单位 |
| 2 | `running-left` | 0–7 | 120×7 + 220 | 对应向左达到 4 个屏幕坐标单位 |
| 3 | `waving` | 0–3 | 140×3 + 280 | 浮窗源码有 `first-awake` 映射，其他入口待实测 |
| 4 | `jumping` | 0–4 | 140×4 + 280 | 动作表与离线 QA 已定位，浮窗稳定触发方式待确认 |
| 5 | `failed` | 0–7 | 140×7 + 240 | 浮窗本地任务分支的失败 turn 或特定系统错误 |
| 6 | `waiting` | 0–5 | 150×5 + 260 | 等待批准、用户输入或允许执行计划等 |
| 7 | `running` | 0–5 | 120×5 + 220 | 浮窗活动中的任务，优先级低于等待和失败；角色语义是专注工作 |
| 8 | `review` | 0–5 | 150×5 + 280 | 浮窗分支中的未读 turn 或成功通知映射；受状态优先级影响 |
| 9 | 注视 A | 0–7 | 指针选格 | 000、022.5、045、067.5、090、112.5、135、157.5 |
| 10 | 注视 B | 0–7 | 指针选格 | 180、202.5、225、247.5、270、292.5、315、337.5 |

000 朝上，090 朝屏幕右，180 朝下，270 朝屏幕左。源码按中心向量将角度舍入至最近的 22.5°，再取行列。近中心时函数返回空方向，由调用侧回退。16 格顺序可合成离线 QA 循环。浮窗指针选格没有固定逐帧轮播时长。标准播放辅助函数还包含状态持续循环、非循环动作三遍后切 idle、以及该函数 idle 数组基础时长 ×6 的分支。其在各界面、模式和前后台下的实际播放取法、覆盖优先级及触发次数留给 P5。

## 注册与静态证据

- 当前 app bundle `.vite/build/early-bootstrap-7-04ae72fad1d22c3a.js` 的本地读取分支扫描 Codex 数据目录下 `pets/` 中的 `pet.json`，读取其图集并按 PNG/WebP 头部与版本对应尺寸判定。还读取旧 `avatars/` 路径。清单版本缺省为 1，因此 2288 高必须明确声明版本 2。本地选择 ID 由目录名派生为 `custom:<目录名>`。
- 清单按随附契约使用 `id`、`displayName`、`description`、`spriteVersionNumber: 2`、`spritesheetPath: "spritesheet.webp"`。P5 分别创建三个新目录，并在 Settings → Pets 刷新，分别选择与显示。当前存在三套 Asuka 本地包；历史运行报告与本次目录和哈希检查属于不同证据。
- 播放和注视代码位于 `webview/assets/async/49792.d8d33ace73.js`，任务活动、拖动和首次唤醒映射位于 `webview/assets/async/268134.7ec32865a9.js`。成员哈希见证据 JSON。准确触发路径以各界面的实测补齐。
- 官方说明确认桌面创建使用 `hatch-pet`、刷新和本地存储。该页另有 Web 上传说明，适用范围不同。 [OpenAI Pets 文档](https://learn.chatgpt.com/docs/pets#create-a-custom-pet)
