# CODEX_CLOUD_ART_PILOT_REPORT

2026-11-27 · REI-PET-CODEX-CLOUD-ART-PILOT

**真实角色试验建立了六帧动作与四方向样本的云端流程。** 10 张选用试验帧达到 `STRUCTURE_PASS`，可作为 `ART_CANDIDATE` 进入 `PENDING_HUMAN_REVIEW`。试验结果不计入 P4-B-FIX 或 P4-C 正式生产进度。

## 固定来源

- 私有仓库 `waynewayne893/rei-desktop-pet`，分支 `feat/p4b-review-center-v1`，提交 `6fd635a3d83336a4b5445e021a7f0eddfdf39fc6`。
- 校服与黑服均引用仓库冻结派生母版。waiting 生成另引用既有六帧原始条带，GIF 使用仓库已登记的六张标准帧作为旧版。四方向与驻足姿势依据 `CODEX_PETS_COMPATIBILITY.md`、`REI_P4_ACTION_SPEC.md` 和 `HANDOFF_P4C.md`。
- 试验产物独立存放于 `/workspace/scratch/rei-art-pilot`。冻结资产、171 帧和三套标准图集通过仓库 CLI 复验。固定提交检出和原工作检出 Git 状态均为空。 [复验记录](evidence/protected-baseline-verify.json)

## T1｜校服 waiting 六帧

| 项目 | 结果 |
| --- | --- |
| 原始输出 | 调用 Image Generation 返回 2172×724（3:1）RGBA PNG，847,506 像素全透明。图中有六个独立的实心前景区。 [原始条带](raw/waiting-attempt-01.png) |
| 分帧门禁 | 原图按 Alpha > 0 的严格检查先得 `FAILED`。实测画布边缘和五道分隔线的 Alpha 最高均为 1/255。保留原始字节，登记时只清除等于 1 的 Alpha 后，六格有效轮廓互相分离且未触及画布边界。 [严格原图检查](evidence/waiting-attempt-01-strict-alpha-qa.json) |
| 标准帧 | 6×192×208 RGBA，六帧使用同一比例和共同纵向落脚基准。实体高度实测均为 187 px，距 188 px 基线 1 px。脚底锚点实测 x=95.5–96.5、y=194–195。 [结构检查](evidence/waiting-attempt-01-qa.json) |
| 身份与动作 | 目视可辨识蓝发、双白发夹、红瞳、红领结、蓝裙与袜鞋。举掌始终由角色左手完成，右手留在身前。F5 手指收拢略显生硬，建议在人工验收中重点看 F5→F6 的收手节拍及手指细节。 [手部近看](evidence/waiting-attempt-01-hands.png) |
| 循环 | F6 回到接近 F1 的交握姿态。首尾实心轮廓 IoU 为 0.8837，旧版为 0.8695。IoU 只衡量轮廓重合度，动作自然度由人工观看 GIF 裁定。两版同步重放 150/150/150/150/150/260 ms。 [浅底对比 GIF](evidence/waiting-attempt-01-comparison-light.gif) · [深底对比 GIF](evidence/waiting-attempt-01-comparison-dark.gif) |
| 美术与边缘 | 明暗底可检查轮廓、画风与服饰线条。样本保留原角色特征，精度及帧间美术一致性仍待人工确认。 [明暗接触表](evidence/waiting-attempt-01-edges.png) |

## T2｜黑服四方向

T1 标准帧通过离线技术检查后开始。两次生成均使用冻结黑服派生母版。第一次原图外边界 Alpha 达 2/255，超出本试验的 1/255 清理规则，记为 `FAILED`。第二次要求扩大角色与画布边缘的距离，原始边界 Alpha 最高为 1/255，四格通过同一登记检查。 [第一次原图](raw/directions-attempt-01.png) · [失败记录](evidence/directions-attempt-01-qa.json) · [第二次原图](raw/directions-attempt-02.png) · [通过记录](evidence/directions-attempt-02-qa.json)

| 角度 | 目视观察 |
| --- | --- |
| 000° | 抬头向屏幕上方看。 |
| 090° | 头与眼睛向屏幕右侧转。 |
| 180° | 低头垂眼。建议人工确认仅看眼部时，向下的读向是否仍清楚。 |
| 270° | 头与眼睛向屏幕左侧转。 |

四格高分原图可读红色 `09`，角色右手仍跨身体扶左臂，左手垂下。090° 和 270° 来自不同生成格，未做镜像处理，二者标准帧也不满足像素镜像相等。四格实体高度为 188–189 px，脚底 x=95.5–96.0、y=195–196，与现有黑服 188 px 立姿和 y=195 基准相差至多 1 px。 [明暗接触表](evidence/directions-attempt-02-contact.png) · [面部与 09 近看](evidence/directions-attempt-02-face-and-09.png)

## T3｜处理与检查口径

- Python 3.12.14 + Pillow 13.0.0，使用仓库 `rei_atlas_tools.py` 的单格分析函数。当前云端没有可调用的 `hatch-pet`，本轮结论限于离线检查。
- 直接保存生图返回的 PNG。利用原生 Alpha 的横向间隔裁切，等比缩放后在 192×208 透明画布平移登记，以脚底带中点估计 x、实心框下边界（右开区间）估计 y。waiting 同行使用首帧地线，四方向使用同一比例并逐格按鞋底平移。动作与方向来自生成原图。
- 选用的 10 帧透明边框完整、Alpha=0 处 RGB 全零、Alpha≥128 的前景各只有一个 8 连通分量。按 Alpha>0 计算时，数帧还存在由缩放保留的低 Alpha 小分量，最大 7 px，最高 Alpha 4/255。明暗板上未见明显独立轮廓，边缘美术保留人工验收。 [小分量记录](evidence/detached-alpha-components.json)
- `STRUCTURE_PASS` 指当前离线技术门禁通过。 `ART_CANDIDATE` 指可供审阅的试样。 `PENDING_HUMAN_REVIEW` 指人物、动作及边缘美术仍待人工裁定。 `FAILED` 用于未过门禁的中间检查或试样。失败产物保留在交付包中作为证据。

## T4｜交付

- [试验清单与资产 SHA-256](CODEX_CLOUD_ART_PILOT_MANIFEST.json)
- [包含原图、对比 GIF 和审阅功能的 Review Center 离线包](../Review-Center/rei-review-center-v1.0-offline.zip)
- [完整文件校验清单](SHA256SUMS)

GitHub 发布未执行。此次交付只位于云端 scratch。既有 171 帧、冻结母版、已验收黑服右跑和 Review Center 数据均通过工作树状态检查。
