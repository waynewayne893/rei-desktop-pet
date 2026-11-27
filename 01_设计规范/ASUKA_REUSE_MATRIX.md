# Asuka 工程复用矩阵

A 可直接调用通用能力，B 需参数化或适配，C 需为 Rei 独立设计，D 禁止迁移。P2 完成分类，落地排入后续阶段。桌面以当前随附 `hatch-pet` 为执行入口。

| 类别 | 项目及原工程证据 | Rei 落地 |
| --- | --- | --- |
| A | 网格和状态协议。Asuka 两套标准 atlas 经现随附校验器复跑通过 | 192×208 单格、标准九行、16 方向、顺时针排位、已验证的 v2 尺寸。照当前桌面装配器加入中性参考格 |
| A | Python/Pillow 通用图集工具。现随附 `compose_atlas.py`、`assemble_extended_atlas.py`、`validate_atlas.py`、`make_contact_sheet.py` | 直接从随附技能目录调用并记录包版本与脚本哈希，在 Rei 每个形态目录获得输出 |
| A | QA 方法。原工程 `qa/{pet-quality,direction-continuity,direction-semantics,direction-blind-validation}.json` | 继承分层流程：结构、透明边缘与裁切、逐行运动、四基准方向、两行跨界、独立盲检、最终编码和本地运行 |
| B | `finish_standard_rows.py` 依赖硬编码 Work Pets 插件路径，合并已验收帧并调用检查、装配、预览 | 复用参数传递与哈希保护思路。首选随附 CLI，仅将重复的路径与输入验证抽成轻薄入口。旧校验器作差异诊断 |
| B | `render_final_previews.py` 使用 Pillow 和 Work Pets 帧时序，MP4 调用 PATH 上的 FFmpeg | 先用随附 GIF 预览，MP4 仅在已有编码器可用时选用。已实测 Python 3.14.6、Pillow 12.3.0、libwebp 1.6.0。当前 PATH 未发现 ffmpeg、magick |
| B | 旧背景处理与 `school/qa/clean-row-10-v4-matte.py` 带单次候选坐标和素材假设 | 三张 Rei 母版都是不透明渐变且带根部软影。P3 分别提取派生 Alpha，保护发尖、白服、袜鞋、手臂间隙。优先保留后续条带原生 Alpha。确有色键残边才选桌面随附脱溢色工具并验证 |
| B | 帧适配。随附提取识别完整连通姿态，合成器会缩放超格并居中 | 先统一角色头部比例、缩放、脚底锚点、动作安全区与留白，再用装配器。跳跃保留纵向位移，注视两行共用变换。避免逐帧强行铺满和自动居中造成抖动 |
| B | 安装模板。原有 `delivery/asuka-v2_20261026/<id>/pet.json` 和同目录 WebP | 复用字段模板并改写三套独立 ID、名称与描述。注册前确认目标目录不存在，安装后对最终文件做哈希校对与重启测试 |
| C | 角色动作、表情、基本节奏、眼头分工、服装细节与左右动作 | 三套单独做角色动作表与注视机制，分别以各自冻结母版为视觉来源。黑服保留人物右扶左的关系与 09 字形，左右跑默认独立设计，镜像须证明语义及编号无损 |
| D | Asuka 图像、帧、表情、提示词中的造型、最终包、ID、Asuka 身份和运行状态证据 | 保留在原路径供审计。混合整行复制脚本 `mix_rows_test.py` 及任务中换服装方案排除在 Rei 范围之外 |
| D | Codex 安装目录、已有宠物目录、本地活跃项、用户数据、授权不明的外部素材 | 原地保留。P6 对仓库内容做授权梳理，各用户配置、凭据和不适合再分发的素材留在本机 |

原工程源码通过 `rg` 和逐文件读取核实。codebase-memory 查得原仓库无索引，因此本审计使用源码回退。历史脚本含覆盖式写入或固定路径，执行证据来自当前无写入校验器；未运行会改动原工程的制作脚本。

参考 [兼容性](../09_项目文档/CODEX_PETS_COMPATIBILITY.md) · [证据](../07_QA验收/ASUKA_P2_READONLY_EVIDENCE.json)
