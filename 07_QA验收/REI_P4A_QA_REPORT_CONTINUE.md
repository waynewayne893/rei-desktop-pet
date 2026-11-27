# REI-PET-P4-A｜白服补齐与候选验收更新

**结构交付 42/42 帧。动态美术待用户与主控验收，阶段维持 PARTIAL。** 本更新依据 REI-PET-P4A-MAIN-REVIEW-01。原 P4-A 报告和原资产清单保留，记录补齐前的状态。

## T1｜白服 idle 重试

指定的 P3-FIX 白服 RGBA 是本次两条源图唯一的人物设计参考。校验先读取生成文件原字节，逐个复算并保存原始图，随后执行安装版 `hatch-pet` 的 `load_native_alpha_image`。重试通过后再执行 `extract_strip_frames.py` 与 `inspect_frames.py`，结构检查无警告。没有用全局 Alpha 拉伸或遮罩挽救拒收图。帧提取按连通主体分离并沿用等比例注册，白服 Alpha 清理门槛参数为 0。

| 源图 | Alpha 范围 | 全透明像素 | 四角 | 处理状态 |
| --- | --- | ---: | --- | --- |
| idle 首次 | 178–253 | 0 | 184、178、184、179 | 拒收并保存原件 |
| idle 唯一重试 | 0–255 | 752,220 | 0、0、0、0 | 6 帧候选 |
| running-right 首次 | 0–255 | 949,954 | 0、0、0、0 | 8 帧候选 |

白服待机可见眼睑逐步降低、闭眼、睁开，双臂持续下垂。可见实体高度为 187–189 px，中性首帧 188 px。原生 192×208 六帧使用共享等比尺度和底界 195 锚点。白色套装、橙绿细节和胸前 00 在源图可见。 [待机原生 Alpha 前后](P4-A/continue/white-idle-alpha-before-after.json) · [源图脸型与胸前细节](P4-A/continue/white-source-face-and-chest.png)

## T2｜白服 running-right

在重试 idle 源及帧结构通过后生成并验收。八帧均向屏幕右，源图和原生帧格可见躯干前倾、膝盖屈伸、举臂摆动以及支撑与腾空变化。装甲配色、白发饰、蓝发和胸前 00 保持可辨，部分侧身帧的编号在 192×208 下较小。逐帧观察可区分着地、屈膝和抬脚，左右脚在个别遮挡帧的交替与首尾过渡留给实际 GIF 美术验收。第 4 帧最低实体点在 y=183，离基准 12 px，下一帧回到 y=195。顶边最少 4 px 全透明，两侧最少 49 px，八帧边界全透明。 [白服两行逐帧表](../04_白色战斗服/P4-A/P4-A-contact-sheet.png)

## T3｜受保护候选的补充检查

- **校服离地**。第 4、8 帧最低实体点距 y=195 分别为 9、12 px。相邻帧为 0–1 px。第 8 帧原时序为 220 ms，容易突出最后一次离地，建议在 GIF 里先检查第 7→8→1 帧是否显得悬停，若确认再只研究相关过渡。 [离地与循环逐帧证据](P4-A/continue/preserved-gait-transitions.png)
- **校服 Alpha 48**。按同源、同一帧注册位置重放 0 与 48 两档，48 档逐帧与原候选相等。每帧头部区域有 13–38 个像素跨到 Alpha 128 以下，完全不透明像素被清零的计数为 0。深浅底放大查看未见呆毛或发梢断裂，细浅边有变窄。若播放发现局部闪烁，仅针对具体帧检查，不调整整行。 [同位清边对照](P4-A/continue/school-alpha48-before-after.png)
- **黑服扶臂与深底**。抽看向右第 1、3、5、8 帧，右手扶左臂的接触关系持续可辨，动作主要集中在髋膝和双脚，上身较克制。深色底 `#263242` 中，抽样帧下半身 Alpha≥128 的像素有 53.4%–58.1% 与背景亮度相差小于 12。红靴缘仍可辨，腿部外缘与步态用浅底更容易看清。人工播放若确认肩、躯干过于固定，建议只比较该移动行的肩髋微调选项。 [扶臂与明暗底](P4-A/continue/black-forearm-and-contrast.png)
- 原校服与黑服的 28 帧以及 22 个源图、预览及总接触表记录逐一复算哈希，与上一轮清单一致。冻结源、P3/P3-FIX、明日香工程与已安装宠物亦按既有清单复核。 [28 帧哈希保护证据](P4-A/continue/protected-28-frame-hashes.json) · [量化视觉证据](P4-A/continue/preserved-visual-audit.json)

## T4｜实际文件

42 张原生 PNG 均解码为 192×208 RGBA，四边完全透明、无透明区残留 RGB、每帧主体连通且每行帧像素不重复。12 个 GIF 均复解码核对 6/8 帧数、循环与播放时长。指定动作状态与原始帧次序保持。结构通过只用于确定可提交的候选。 [注册结构 QA](P4-A/continue/registered-42-structure.json) · [完整更新资产清单](REI_P4A_ASSET_MANIFEST_CONTINUE.json)

| 形态 | 待机原生 GIF | 右移动原生 GIF | 逐帧接触表 |
| --- | --- | --- | --- |
| 校服 | [深底](../03_校服绫波丽/P4-A/selected/idle/idle-dark.gif) · [浅底](../03_校服绫波丽/P4-A/selected/idle/idle-light.gif) | [深底](../03_校服绫波丽/P4-A/selected/running-right/running-right-dark.gif) · [浅底](../03_校服绫波丽/P4-A/selected/running-right/running-right-light.gif) | [明暗底逐帧](../03_校服绫波丽/P4-A/P4-A-contact-sheet.png) |
| 白服 | [深底](../04_白色战斗服/P4-A/selected/idle/idle-dark.gif) · [浅底](../04_白色战斗服/P4-A/selected/idle/idle-light.gif) | [深底](../04_白色战斗服/P4-A/selected/running-right/running-right-dark.gif) · [浅底](../04_白色战斗服/P4-A/selected/running-right/running-right-light.gif) | [明暗底逐帧](../04_白色战斗服/P4-A/P4-A-contact-sheet.png) |
| 黑服 | [深底](../05_黑色战斗服/P4-A/selected/idle/idle-dark.gif) · [浅底](../05_黑色战斗服/P4-A/selected/idle/idle-light.gif) | [深底](../05_黑色战斗服/P4-A/selected/running-right/running-right-dark.gif) · [浅底](../05_黑色战斗服/P4-A/selected/running-right/running-right-light.gif) | [明暗底逐帧](../05_黑色战斗服/P4-A/P4-A-contact-sheet.png) |

- [√] 白服原生 Alpha 重试与两行样板
- [√] 42 帧及 12 个 GIF 结构复核，已有资产保护
- [ ] 三套角色动态美术验收
- [ ] 后续阶段授权

停止于 P4-A。
