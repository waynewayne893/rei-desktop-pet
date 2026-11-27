# Rei Desktop Pet V1.0｜P2 审计报告

**建议裁定：PARTIAL，待主控独立验收。** 原工程只读审计、三图冻结登记与备份、目录初始化、复用矩阵及路线均已完成。桌面安装版的几何和大部分状态映射已通过静态核对，但随附 v2 打包校验额外要求中性格。旧版 73 格资产不能直接通过该校验，且本轮没有实测当前应用的逐项触发及重启。下载前的上游文件来源也未独立追溯。

## T1｜原工程和现有安装

- 原工程 `D:\HuaweiMoveData\Users\86191\Desktop\Codex_Asuka`，分支 `main`，HEAD `1e52fc5c20b947a2570695f94c968990c32fd025`，本地 origin `https://github.com/waynewayne893/asuka-desktop-pet.git`。
- 开工及初始化后 Git 状态相同。预存修改为 `AGENTS.md` 与 `docs/08-混合双形态最小测试_工作稿.md`，预存删除为 `references/approved_baselines/asuka_school_mode_baseline_v2.png`。HEAD 中仍可只读取得该 PNG，2,272,395 字节，SHA-256 `3f3062bc338ac9c9fbb7bbb319b1b7abdab5f8d756dd469ab6838963cbd42524`。两次 `git diff --binary HEAD` 输出哈希相同，详见证据 JSON。
- `work/` 被原仓库忽略，`git ls-files work` 无条目。现场脚本、逐帧、QA 和未清边图依赖本机工作目录。以该仓库的 Git 提交单独恢复，无法重建全套制作现场。
- `A-明日香双形态_v1.0_项目完成说明.md` 是结项汇总。较具体的历史证据见 `docs/07-最终接入与验收报告_工作稿.md`、各形态 `qa/` 和混合版 `mixed-test/qa/runtime-observation.json`。两只独立包曾由用户确认可选可播放。混合包曾由用户观察一次约 20.3 秒普通任务，范围限这次体验。历史校服和战斗服 QA 均有通过记录，另留有注视过渡和盲检歧义警告。

### 素材实际解码

下表路径相对于原工程。每个副本的绝对路径、字节数、模式、Alpha 极值和像素统计、逐行占用列及完整 SHA-256 见 [ASUKA_P2_READONLY_EVIDENCE.json](../07_QA验收/ASUKA_P2_READONLY_EVIDENCE.json)。

| 位置或文件 | 实际格式与尺寸 | 实测结构 |
| --- | --- | --- |
| `work/phase3_20261025/{school,work}/decoded/base.png` | PNG，1024×1536，RGBA | Alpha 0–254，制作输入 |
| `work/phase3_20261025/{school,work}/decoded/running.png` | PNG，2172×724，RGBA | Alpha 0–255，工作态条带。另有同名 layout guide 与候选目录，应用行对应的是图集行 7 |
| `work/phase3_20261025/{school,work}/final/spritesheet-standard.png` | PNG，1536×1872，RGBA | 57 格有非零 Alpha，15 格全透明 |
| 同目录 `spritesheet-extended-unclean.png`、`spritesheet-extended.png`、`spritesheet-extended.webp` | PNG 或 WebP，1536×2288，RGBA | 各 73 格有非零 Alpha，15 格全透明。相同占用图形无法判断边缘清洁度 |
| `delivery/asuka-v2_20261026/{asuka-school,asuka-work}/spritesheet.webp` | 静态 WebP，1536×2288，RGBA | 两套各 73 格，逐一等同其最终图集与本机安装副本 |
| `work/phase3_20261025/mixed-test/final/spritesheet.webp` | 静态 WebP，1536×2288，RGBA | 73 格，等同本机混合测试安装副本 |

本机安装根为 `C:\Users\86191\.codex\pets`。枚举到 `asuka-school`、`asuka-work`、`asuka-mixed-test` 三只本地包。每个目录均含 `pet.json` 与 `spritesheet.webp`，清单版本为 2。各清单也与对应交付或混合最终版逐字节一致。原交付包 `SHA256SUMS.txt` 的 5 项全部复算匹配。

## T2｜当前兼容性

本机 MSIX `OpenAI.Codex 26.1120.6357.0`。Pillow 自行解码帧分布，随附 `hatch-pet/scripts/validate_atlas.py` 另行复跑 14 项。2 张标准图通过，12 个历史 v2 副本均只报 `idle row 0 column 6 is empty or too sparse (0 pixels)`。本机打包器把该格用作中性注视，因此桌面打包占用为 57 个动作帧 + 16 个方向帧 + 1 个中性参考格。应用主播放表保留 6 个 idle 帧。详见 [兼容性审计](CODEX_PETS_COMPATIBILITY.md)。

## T3｜冻结母版

三张 PNG 已在 `00_原始美术母版/` 定位并人工视觉核对。均为单人全身、1024×1536、RGB、无 Alpha 和 PNG tRNS。校服为手在身前自然交握的独立画布，当前无并排裁切项。白色为 00 驾驶服双臂下垂，黑色有 09 标识且右手扶左臂。背景为浅冷色渐变与脚下柔影，边缘细节应在 P3 逐图验证。已建立同字节备份。[冻结登记](../00_原始美术母版/REI_ART_FREEZE_MANIFEST.json)

主控会话《复用路径开发绫波丽》保留了用户对三版的下载与冻结确认，且该会话列出的目标文件名与工作区三个文件完全一致。按文件名和长度检查当前 Windows Downloads，未找到对应 PNG 副本。主控聊天可读取的两张同尺寸 PNG 附件是 RGBA，编码哈希与解码 RGB 均与三份工作区母版不同。以工作区现存版本登记，下载前源路径和工作区以前的哈希仍待补证。

## T4–T6｜复用、隔离与后续

复用决策见 [矩阵](../01_设计规范/ASUKA_REUSE_MATRIX.md)。Rei 根目录为 `D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet`，十个分区均已就绪。Rei、Asuka 与安装目录解析为三个独立路径，母版目录和备份目录为普通目录。两次检查的 49 个原工程及安装路径、11 个历史 QA 报告、3 个工作区源图和 Git 状态一致。范围为所列文件与 Git 工作区快照。纯工具输入来自原路径读取。

- [√] T1 原工程、历史运行记录、安装包及哈希审计
- [√] T2 当前规格、现有资产和打包校验差异复核
- [√] T3 三图冻结登记、视觉核对、字节备份
- [√] T4 复用矩阵
- [√] T5 十个独立工程目录
- [√] T6 P3–P6 路线与交接
- [ ] 独立验收、当前版本逐项播放复测、候选 Rei 包的当前校验及重启验收

P2 的六件交付物按职责落在 `00_原始美术母版/`、`01_设计规范/` 和 `09_项目文档/`。证据在 `07_QA验收/`。本轮目录初始化采用现有工作区，Git 仓库初始化与私有远端交付列在 P6。P2 停止于主控验收前。[路线](REI_PROJECT_ROADMAP.md) · [P3 交接](HANDOFF_P3.md)
