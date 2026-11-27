# REVIEW_CENTER_QA_REPORT.md｜Visual Review Center V1.0 实测 QA 报告（T3–T5）

- **任务编号**：`REI-PET-CLOUD-P4B-REVIEW`（T3–T5）
- **开发分支**：`feat/p4b-review-center-v1`
- **验证日期**：2026-11-27
- **实测引擎**：Playwright `1.65.2` + 无头 Chromium（真实 `file://` 双击打开协议，无 HTTP 服务器、无跨域代理、无 Node.js）
- **综合结论**：**`REVIEW_CENTER_QA_PASS`（工具与离线包全部实测通过；注意：仅代表验收工具就绪，不代表 163 帧候选已完成人工美术终审）**

---

## 1. 可访问性验证结论（T4）

- **云端受保护网页托管评估**：Antigravity Cloud 沙箱仅提供容器本地执行环境，不提供面向用户外网可访问且受权限保护的仓库目录静态托管 URL；依据红线禁止开启公开 GitHub Pages 或上传素材至第三方平台。
- **实际交付入口（双击即开、零 CORS、零框架、零 Node.js）**：
  1. **离线独立压缩包（推荐）**：`07_QA验收/Review-Center/rei-review-center-v1.0-offline.zip`（`11,964,244` B，内置 `192` 个文件：HTML/CSS/JS + 模板 + 使用手册 + 全部 186 张仓库真实素材图；解压后直接双击 `rei-review-center-v1.0/index.html` 即可运行）。
  2. **仓库内直接入口**：`07_QA验收/Review-Center/index.html`（通过 `assets/review-data.js` 同步注入数据，无任何 `fetch()` 跨域请求，直接双击打开）。

---

## 2. 双目标端到端浏览器实测结果（T5）

测试同时覆盖两个真实 `file://` 目标：
1. **仓库相对路径目标**：`file:///.../07_QA验收/Review-Center/index.html`
2. **完全隔离离线解压目标**：将 `rei-review-center-v1.0-offline.zip` 解压至 `/tmp/rei-review-offline-test/` 后打开 `file:///tmp/rei-review-offline-test/rei-review-center-v1.0/index.html`（不依赖仓库任何外部路径）

| 实测项 | 仓库 `file://` | 离线 ZIP 解压 `file://` | 实测详情 |
| --- | :---: | :---: | --- |
| 基线治理校验（`STRUCTURE_PASS` 不自动转 `ACCEPTED`） | **PASS** | **PASS** | 初始仅 `rei-black::running-right`（8 帧）为 `ACCEPTED`；其余 26 动作（163 帧）均为 `PENDING` |
| 27 条动作统一索引可访问性 | **PASS** | **PASS** | 27/27 动作逐一切换与渲染正常 |
| 全部 171 帧真实解码尺寸核验 | **PASS** | **PASS** | 171/171 张 `<img>` 真实解码尺寸均为 `192×208`，0 坏图 |
| 动画播放顺序与严格冻结帧时序 | **PASS** | **PASS** | 全部 9 行帧时长与 `REI_P4B_ASSET_MANIFEST.json` 逐项一致；`idle` 实测首帧调度 `280 ms` 并顺次推进至 `F1` |
| 三形态同状态并排同步播放 | **PASS** | **PASS** | `rei-school` / `rei-white` / `rei-black` 3 路 `192×208` 同步渲染，并支持就地状态切换 |
| 浅底 / 深底 / 透明格背景切换 | **PASS** | **PASS** | `#singleStageViewport` 正确切换 `bg-light` / `bg-dark` / `bg-checker` |
| 原生 1× / 2× / 4× 缩放与逐帧控制 | **PASS** | **PASS** | 实测渲染盒尺寸精确为 `192×208`、`384×416`、`768×832`（修复了初测发现的 `4×` flexbox 横向压缩缺陷）；上一帧/下一帧/播放/暂停正常 |
| 新旧候选与锁定 P3/P3-FIX 母版对比 | **PASS** | **PASS** | `rei-black/running-right` 新旧 8 帧对比、`rei-white/idle` attempt-01 vs attempt-02 条带对比及 P3/P3-FIX 母版图 100% 加载解码正常 |
| 局部细节放大镜与 00/09 标识检查 | **PASS** | **PASS** | `4×/6×/8×` Canvas 放大镜实测渲染有效细节像素；白服 `00` 与黑服 `09` 高分专检拼图均正常解码 |
| JSON 验收记录导入导出往返一致性 | **PASS** | **PASS** | 修改状态与意见 → 导出 JSON → 重置基线 → 重新导入 → 二次导出逐项（27 动作状态、备注、哈希、帧统计）100% 往返一致 |
| **资产哈希变化后旧版验收自动失效** | **PASS** | **PASS** | 篡改导出 JSON 中已标 `ACCEPTED` 的 `rei-white::idle` 动作/帧哈希后导入：自动识别 `invalidatedCount = 1`，将其状态强制回退为 `PENDING` 并标记 `invalidated = true`、`stale_previous_status = "ACCEPTED"`，顶部与面板均显示紫底失效告警 |
| Markdown 验收摘要生成 | **PASS** | **PASS** | 完整输出 3×9 验收表、帧数进度、`HASH_INVALIDATED` 标记及 `NEEDS_FIX`/`REJECTED` 清单 |
| 浏览器控制台与网络零报错 | **PASS** | **PASS** | `console_errors = 0`、`page_errors = 0`、`failed_requests = 0`（零 `file://` CORS 报错） |

---

## 3. 交付物与完整性哈希

| 文件 | 路径 | 体积 (Bytes) | SHA-256 |
| --- | --- | ---: | --- |
| 页面入口 | `07_QA验收/Review-Center/index.html` | `16,580` | 以本分支提交实测为准 |
| 样式表 | `07_QA验收/Review-Center/assets/styles.css` | `18,658` | 以本分支提交实测为准 |
| 主程序逻辑 | `07_QA验收/Review-Center/assets/app.js` | `48,257` | 以本分支提交实测为准 |
| 同步数据索引（仓库版） | `07_QA验收/Review-Center/assets/review-data.js` | `102,702` | `96e972d3af91d5d729fb60f71df85fcd851b6e6a319af8f18f4bcd47619f9d28` |
| 标准验收模板 JSON | `07_QA验收/Review-Center/REI_ART_REVIEW_TEMPLATE.json` | `31,448` | `38859e98a1d473aadeca4987b674f8a792ca0a0309fb94269ce58255eaf07093` |
| **独立离线 ZIP 包** | `07_QA验收/Review-Center/rei-review-center-v1.0-offline.zip` | `11,964,244` | `e9c84960912fba763c53b4bb12cfc7733d4ac4b7cc9e9062f2f7c1675607a012` |
| 使用手册 | `07_QA验收/Review-Center/REVIEW_CENTER_README.md` | `5,280` | 以本分支提交实测为准 |
| 工具链复验报告 | `07_QA验收/Review-Center/CLOUD_TOOLCHAIN_VERIFICATION_REPORT.md` | — | 以本分支提交实测为准 |

---

## 4. 原始资产零修改与停止边界核验

- 重新执行 `python3 06_共用工具/rei_atlas_tools.py verify` 返回退出码 `0`（`ok: true`，6/6 冻结与备份、3/3 派生母版、171/171 帧、3/3 标准图集哈希全部零变化）。
- 未生成新动画素材，未启动 `P4-B-FIX`、正式 `P4-C`/`P4-D`/`P5`/`P6`，未修改明日香工程，未安装宠物，未公开仓库，未发布 `v1.0.0`。
