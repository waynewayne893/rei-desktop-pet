# REVIEW_CENTER_README.md｜Rei Desktop Pet 可视化人工验收中心 V1.0 使用手册

> **用途定位**：专供用户独立完成 **P4-B 3×9（27 条动作 / 171 帧）** 动态美术人工终审，无需切回原 Windows 开发工程、无需向 ChatGPT 逐个上传 GIF、无需安装 Node.js 或任何前端框架。  
> **安全与合规边界**：纯本地离线静态页面（原生 HTML + CSS + JavaScript），不使用公开 GitHub Pages，不上传素材至第三方平台，不依赖浏览器跨域 `fetch()`。

---

## 1. 可访问性验证结论与两种直接打开方式（T4）

- **Antigravity Cloud 云端托管验证**：Antigravity Cloud 沙箱仅运行容器本地进程，不提供面向用户外网直连且带鉴权的静态网页托管入口（禁止对外公开仓库或 GitHub Pages）。
- **已交付的两种零依赖本地打开方式（均支持直接双击 `index.html`，零 CORS 报错）**：
  1. **推荐｜一键下载独立离线包**（无需克隆仓库、无需原 Windows 工程）：
     - 从 GitHub 私有仓库下载 `07_QA验收/Review-Center/rei-review-center-v1.0-offline.zip`；
     - 解压至任意文件夹；
     - **直接双击 `rei-review-center-v1.0/index.html`**（Chrome / Edge / Firefox / Safari 均可直接打开）。
  2. **仓库内直接打开**（若本地已克隆本仓库）：
     - 直接双击打开 `07_QA验收/Review-Center/index.html`（通过相对路径直接引用仓库内 171 帧原图与拼图）。

---

## 2. 功能清单（12 项全部实装）

1. **27 条动作统一索引（3 形态 × 9 状态）**：左侧边栏按 Row 0–8 分组索引 `rei-school`（校服）、`rei-white`（白服 00）、`rei-black`（黑服 09），支持按状态（全部 / 待审 / QA 关注 / 已通过 / 需修复 / 拒收）与形态快速筛选。
2. **三形态并排同步播放**：点击顶部 **「三形态并排同步」** 或任意动作行右侧 **「三形态并排」**，三套形态按同一严格冻结帧序与单帧时长同步播放，可就地切换状态。
3. **浅底 / 深底 / 透明格切换**：一键切换 `#f0f3f9` 浅底、`#131a26` 深底及透明棋盘格，检查发丝与白服/黑服边缘清洁度。
4. **1× / 2× / 4× 缩放预览**：支持原生 `192×208`、`384×416`、`768×832` 预览，支持「像素锐利」与「`(96,195)` 脚底锚点参考线」开关。
5. **播放、暂停、逐帧与循环**：支持界面按钮与快捷键（`Space` 播放/暂停、`←`/`→` 上/下一帧、`1`/`2`/`4` 缩放、`L` 深浅底切换），底部逐帧条支持点击任意帧定位。
6. **严格冻结帧时序**：严格按照 `07_QA验收/REI_P4B_ASSET_MANIFEST.json` 锁定毫秒时长调度每帧（如 `idle: [280,110,110,140,140,320] ms`、`running-right/left: [120×7, 220] ms` 等），不使用均速轮播。
7. **新旧候选与锁定母版对比**：切至 **「新旧候选与母版对比」** 可直接播放对比 **黑服旧版拒收 `running-right`（8 帧）vs FIX-BLACK 新版（8 帧）**、对照 **白服 `idle` attempt-01 透明缺陷条带 vs attempt-02 修复条带**，并可将全部 27 条动作与锁定 P3 / P3-FIX 派生母版并排核对。
8. **局部细节放大与 `00`/`09` 标识检查**：切至 **「局部放大与 00/09 标识」** 可在任意一帧上以 `4×`/`6×`/`8×` 拖动或一键聚焦胸口 `00`/`09`、面部、手部、脚底锚点，同时内置仓库高分 `p4b-chest-markings-qa-white.png` 与 `p4b-chest-markings-qa-black.png` 专检拼图。
9. **候选版本与资产哈希绑定 + 自动失效保护**：每条动作绑定 `selected_version`、`source_sha256`、`frame_sha256s` 与综合 `action_asset_hash`。导入旧版 JSON 时，如任意单帧或候选版本哈希与当前仓库资产不一致，该条旧验收将**自动标记为失效并回退为 `PENDING`**。
10. **人工验收意见输入与进度统计**：提供 `ACCEPTED`、`REJECTED`、`NEEDS_FIX`、`PENDING` 四态判定、快捷意见标签与自由备注，顶部实时统计动作进度（`/27`）与帧数进度（`/171`），浏览器本地自动保存草稿。
11. **JSON 验收记录导入与导出**：标准格式见 [REI_ART_REVIEW_TEMPLATE.json](REI_ART_REVIEW_TEMPLATE.json)；用户审阅完成后点击 **「导出 JSON」** 保存文件并交给云端 Agent 同步回 GitHub。
12. **Markdown 验收摘要生成**：点击 **「生成 Markdown 摘要」** 一键生成含总进度、3×9 验收表与 `NEEDS_FIX`/`REJECTED` 精确清单的 Markdown 报告，支持复制或下载 `.md`。

---

## 3. 验收口径与基线规则

- **`STRUCTURE_PASS` ≠ 人工 `ACCEPTED`**：工具绝不会将离线结构通过自动转为人工通过。
- **初始基线**：仅 **黑服新版 `running-right`（8 帧，`FIX-BLACK/attempt-01`）** 预设为 `ACCEPTED`（禁止重做）；其余 **26 条动作（163 帧）** 初始全部为 `PENDING`。
- **离线 QA 重点提示的 3 条观察项**（侧边栏带 `QA!` 标记）：
  - `rei-school / waiting`
  - `rei-black / review`
  - `rei-black / waving`

---

## 4. 如何重新生成索引数据与离线包（云端/本地复算）

```bash
python3 06_共用工具/build_review_center.py
```

该脚本仅依赖 Python 3.11+ 标准库，不改动任何冻结母版或 171 帧原始文件。


## Codex Cloud 专项试验入口

打开 `index.html` 后点击「Codex Cloud 专项试验」，也可从解压后的目录直接打开 `pilot.html`。校服 waiting 以相同冻结时序同步对照旧版与试验版。黑服四个方向分别审阅，页面提供明暗底、局部放大以及原图和检查图。

试验页为 waiting 六帧和四个方向保存独立判定。它的草稿和 JSON 与正式 27 条动作分开，请分别导出备份。旧版正式验收 JSON 仍从主页面导入。试验 JSON 同时绑定参考和试验资产版本与 SHA-256，任一绑定变更会让该项回到待审。
