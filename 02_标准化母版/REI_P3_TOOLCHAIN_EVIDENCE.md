# Rei Desktop Pet V1.0｜P3 桌面工具合同

## 版本与校验值

Windows MSIX `OpenAI.Codex` 安装版本 `26.1120.6357.0`。随附技能目录为 `C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0\app\resources\skills\skills\.curated\hatch-pet`。所读的 `SKILL.md` 头部与目录未提供独立的 hatch-pet 版本号。以所属 MSIX 版本和文件 SHA-256 共同锁定这份工具快照。

| 相对路径 | SHA-256 |
| --- | --- |
| `SKILL.md` | `6e37fd125e01e8ee9b93e46ada18a9fa8fbb4cb86f09b531f0a7ac332482a58a` |
| `references/animation-rows.md` | `62643046b18de139c9147bebe79a0912c9cb1b629c535ed4189a07c41b10a3e3` |
| `references/codex-pet-contract.md` | `8c6d1557900c44f267003b9097ad1cfb4e4d29e574ae325c0dd0943b71510d72` |
| `scripts/compose_atlas.py` | `464c198c63e3bc267144056573c8cab3de1f99a4fc5bd47f9e52dffe3f1c88ad` |
| `scripts/assemble_extended_atlas.py` | `207a282f65175bf6088e12770ead1e5f91951b12f3d3772c3cd7c1d418d403c7` |
| `scripts/validate_atlas.py` | `659f48085d4148f23772342a92c0b55ee890a0ef80964b12d935701973ee6a46` |
| `scripts/extract_strip_frames.py` | `e6784f6be9c4fb872383b6a15b5da83ee0bc66a658c7545ec238da5582b5d4c5` |

## 标准动作与方向布局

标准装配器 `compose_atlas.py:11–28` 定义 `COLUMNS=8`、`ROWS=9`、`CELL_WIDTH=192`、`CELL_HEIGHT=208`。对同一文件的 `ROW_SPECS` 进行 AST 字面量解析，得到下表。标准图 1536×1872，57 个有效格，15 个透明空格。

| 行（0 起） | 名称 | 帧数 |
| ---: | --- | ---: |
| 0 | `idle` | 6 |
| 1 | `running-right` | 8 |
| 2 | `running-left` | 8 |
| 3 | `waving` | 4 |
| 4 | `jumping` | 5 |
| 5 | `failed` | 8 |
| 6 | `waiting` | 6 |
| 7 | `running` | 6 |
| 8 | `review` | 6 |

扩展装配器 `assemble_extended_atlas.py:21–47` 定义 8×11，1536×2288。第 433–435 行依索引以除以 8 的整数商和余数定位行列。

```python
row = STANDARD_ROWS + index // COLUMNS
column = index % COLUMNS
```

同一源文件的方向标签按 000 向上开始顺时针排列。

- 行 9，列 0–7 为 000、022.5、045、067.5、090、112.5、135、157.5。
- 行 10，列 0–7 为 180、202.5、225、247.5、270、292.5、315、337.5。

## 中性格 `(0,6)`

装配器 `assemble_extended_atlas.py:404–425` 在未指定外部中性样本时取得可见的中性或 idle 图。第 438–443 行将中性样本放到第 0 行第 6 列，第 455 行写入装配元数据，第 572 行实际调用放置函数。

```python
atlas.paste(neutral, (6 * CELL_WIDTH, 0))
```

校验器 `validate_atlas.py:21,113–141` 只在 2288 高扩展图把该位置加入必用格，并对未用格要求全透明。

```python
EXTENDED_NEUTRAL_LOOK_FRAME = (0, 6)
used = column_index < frame_count or (
    is_extended_atlas and (row_index, column_index) == EXTENDED_NEUTRAL_LOOK_FRAME
)
```

当前读取的 `app/resources/app.asar` 内部成员 `webview/assets/async/49792.d8d33ace73.js` 的 SHA-256 为 `c08e14256566537b430f8c35ea52287e363305711254a1b327b64d1023bf1b0e`。播放器的 v2 表列出 `requiredFramesByRow:[6,8,8,4,5,8,6,6,6,8,8]`，注视映射以 22.5° 就近取方向。核对结论为 **57 个标准动作帧 + 16 个方向格 = 73 个播放表占用格**。在这 73 格之外，打包合同另有 1 个中性参考格，合计 **74 个有内容格，14 个全透明格**。中性格是否会被当前浮窗单独显示，仍需实际运行验收。

## P3 只读复跑

用 Python 3.14.6 调用安装目录内 `validate_atlas.py <现有 asuka-school WebP> --require-v2`。输入为 `C:\Users\<用户名>\.codex\pets\asuka-school\spritesheet.webp`，SHA-256 `51ecce0097b08e17308cbc90bb4dbf8c7353cabb90e33caf970b8d9a8fe80c29`。

- 进程退出码 `1`，`ok=false`。
- 唯一错误 `idle row 0 column 6 is empty or too sparse (0 pixels)`，警告为空。
- 这是对历史安装素材的结构复查。P3 的 192×208 PNG 是单格静态样本，完整候选图集校验及桌面注册验收留在后续阶段。
