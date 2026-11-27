# REI-PET-P4-A｜待机与右移动样板 QA

**建议 `PARTIAL`。** P4-GATE 已通过。校服、黑服共 4 条动作、28 帧是候选。白服首条 idle 因背景 Alpha 不合格停在原始条带，右移动暂不开始。P4-A 当前为 28/42 帧，待白服补齐及三套美术验收。

## 按形态审查

| 形态 | idle | running-right | 观察与待确认 |
| --- | --- | --- | --- |
| `rei-school` | 6 帧 | 8 帧 | 待机依次眨眼并回归，交握、白发饰和浅色袜鞋保留。移动面向屏幕右，屈膝、着地、抬脚、裙摆随动可区分。帧 4、8 的离地幅度较高，循环的支撑脚交替与首尾接续待动态美术验收。 [两行接触表](../03_校服绫波丽/P4-A/P4-A-contact-sheet.png) |
| `rei-white` | 源图拒收 | 暂未生成 | 首次生成的 2172×724 RGBA 上 Alpha 为 178–253，全透明像素为 0。随附 `load_native_alpha_image` 明确拒收。六个可见姿势仍为原始候选，未计入有效帧。下一步需先由用户批准重新生成这一条待机。 [拒收源图](../04_白色战斗服/P4-A/originals/idle/attempt-01/source.png) |
| `rei-black` | 6 帧 | 8 帧 | 待机有眼睑及小幅发梢变化，保持右手扶左臂。向右时上身延续该姿态，髋膝呈不同角度及步幅，靴缘保持红色。深底的黑色腿部对比低，近远脚交替及首尾节奏以浅底 GIF 审查。 [两行接触表](../05_黑色战斗服/P4-A/P4-A-contact-sheet.png) |

## 尺寸、透明度与时序

- 四条已注册行都经真实透明源条带分离，分别使用单一等比行尺度与同一个格锚点 `(96,195)`。校服原条带保有弱 Alpha 残影，以已登记的 Alpha 门槛 48 清理淡底再注册；黑服保留自身 Alpha 内部值。两套待机的 `Alpha≥128` 高度均为 188 px，底界均为 195。右移的脚底高度随离地动作自然变化。
- 校服右移实体高 177–189 px、最低有效顶边余量 5 px。黑服右移实体高 181–188 px、最低有效顶边余量 6 px。所有 28 帧四边全透明，无隐藏 RGB，逐帧 RGBA 唯一。两条右移动作保持原始帧序。
- 随附 `extract_strip_frames.py` 和 `inspect_frames.py` 在四条源图的连通提取上均返回成功、无警告。交付帧另做等比例锚点注册，并复核实际 PNG、GIF。八个深浅底 GIF 均以 192×208 编码，分别复解码了 6/8 帧、毫秒时长和循环标志。接触表用于人工查看，结构通过不能证明步态验收完成。
- 三份冻结原图与 P2 备份、P3/P3-FIX 输入、明日香仓库状态和安装资源经前后哈希复核。未保存任何 P4-B 状态或完整图集。

## 原生 GIF

| 形态 | 待机 | 向右移动 |
| --- | --- | --- |
| 校服 | [深底](../03_校服绫波丽/P4-A/selected/idle/idle-dark.gif) / [浅底](../03_校服绫波丽/P4-A/selected/idle/idle-light.gif) | [深底](../03_校服绫波丽/P4-A/selected/running-right/running-right-dark.gif) / [浅底](../03_校服绫波丽/P4-A/selected/running-right/running-right-light.gif) |
| 黑服 | [深底](../05_黑色战斗服/P4-A/selected/idle/idle-dark.gif) / [浅底](../05_黑色战斗服/P4-A/selected/idle/idle-light.gif) | [深底](../05_黑色战斗服/P4-A/selected/running-right/running-right-dark.gif) / [浅底](../05_黑色战斗服/P4-A/selected/running-right/running-right-light.gif) |

- [√] P4-GATE 与身份确认
- [√] 校服、黑服各两行动作；交互验收候选已生成
- [ ] 白服原生 Alpha 通过后继续该形态
- [ ] 三套 P4-A 美术验收及下一阶段授权

[动作规格](../09_项目文档/REI_P4_ACTION_SPEC.md) · [门禁报告](REI_P4_GATE_REPORT.md) · [P4-A 资产清单](REI_P4A_ASSET_MANIFEST.json) · [P4-B 交接](../09_项目文档/HANDOFF_P4B.md)
