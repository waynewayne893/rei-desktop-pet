# P4D_QA_REPORT.md｜Rei Desktop Pet 三形态最终 v2 扩展图集离线 QA 报告

- **任务代号**：`REI-PET-P4D-AGY-TAKEOVER`
- **任务分支**：`feat/p4d-final-assembly`（基于统一后的 `main`：`44624e1572894f340e9b334ab339d958e7fb9ba2`）
- **版本定位**：**P4-D 候选交付包（非正式 `v1.0.0` 发布；待 ChatGPT 主控独立验收及 Windows P5 实机验收授权）**
- **离线 QA 综合状态**：**`OFFLINE_V2_QA_PASS`（264 / 264 格全量实测通过，0 错误）**
- **平台边界声明（严格诚实）**：本报告**仅记录跨平台 Python 标准库 + Pillow 离线校验结果**；**未执行且未虚构** Windows 原生 `OpenAI.Codex` MSIX `validate_atlas.py --require-v2` 或 Codex Desktop 实机运行测试（均留待 P5 授权后实测）。

---

## 1. 构建与校验环境

| 项目 | 实测值 |
| --- | --- |
| 装配脚本 | `06_共用工具/p4d_assemble.py` |
| 跨平台校验核心 | `06_共用工具/rei_atlas_tools.py`（纯 Python 标准库 + Pillow，零外置依赖） |
| 运行环境 | `Windows 10/11`（独立临时 Git 克隆 `%TEMP%\rei-p4d-takeover-git`，原本地开发工作区与 Asuka 宠物零改动） |
| Python / Pillow / libwebp / zlib | `Python 3.14.6` / `Pillow 12.3.0` / `libwebp 1.6.0` / `zlib 1.3.2` |
| WebP 编码参数 | `format="WEBP", lossless=True, quality=100, method=6, exact=True` |

---

## 2. 三套独立桌宠核心交付件与哈希汇总

| 形态 ID | 显示名称 (`displayName`) | 扩展 PNG (`1536×2288`) | Lossless WebP (`1536×2288`) | 独立安装 ZIP | `pet.json` |
| --- | --- | --- | --- | --- | --- |
| `rei-school` | 绫波丽·校服 | `1,391,577 B`<br>`896a803d...cfcef862` | `1,024,936 B`<br>`e8564b31...756e65ec` | `1,025,776 B`<br>`fa28e137...36fd8e8a` | `296 B`<br>`15aa8533...44214ac` |
| `rei-white` | 绫波丽·白色战斗服00 | `1,463,189 B`<br>`39fb3843...cdc5ad44` | `1,048,278 B`<br>`182369db...50dfe61e` | `1,049,132 B`<br>`0e4e5ade...c39c79f3` | `319 B`<br>`53d53583...2be16bec` |
| `rei-black` | 绫波丽·黑色战斗服09 | `1,295,403 B`<br>`2baac0b9...07dc73b6b` | `946,396 B`<br>`15e65fb6...3fada200` | `947,202 B`<br>`0a795c5b...f4cf5998` | `319 B`<br>`980a4c7c...949d525e` |

- 完整逐文件 SHA-256 清单见：[SHA256SUMS.txt](../../08_正式交付/P4-D-candidate/SHA256SUMS.txt) 与 [P4D_DELIVERY_MANIFEST.json](../../08_正式交付/P4-D-candidate/P4D_DELIVERY_MANIFEST.json)
- 完整 264 格结构与像素级 QA 明细见：[P4D_OFFLINE_QA.json](P4D_OFFLINE_QA.json)

---

## 3. `R0C6` 辅助中性参考格协议依据与溯源

严格依据冻结协议 [REI_PROJECT_ROADMAP.md](../../09_项目文档/REI_PROJECT_ROADMAP.md)（“从验收 idle 提供辅助中性格”）及 [CODEX_PETS_COMPATIBILITY.md](../../09_项目文档/CODEX_PETS_COMPATIBILITY.md)，三套 `R0C6` 均直接采用对应形态已人工验收通过的 `selected/idle/frames/00.png` 原始无修改 RGBA 像素，**不含任何临时测试徽章，未引入 `P4-COMPAT` 临时测试素材**：

| 形态 ID | `R0C6` 来源路径 | 来源 PNG SHA-256 | 解码 RGBA 像素 SHA-256 |
| --- | --- | --- | --- |
| `rei-school` | `03_校服绫波丽/P4-A/selected/idle/frames/00.png` | `1060459b3f468e8302fd40d6bb6b3892df95b4351695274c6a714353a722d1dc` | `5fdb3248db4253c6d69fb10c794957a3eaaf5401d660bda16084b4f847524952` |
| `rei-white` | `04_白色战斗服/P4-A/selected/idle/frames/00.png` | `8ae73126ca709d93ebd4e6d2cca519bbec0b06486905d1fe83117f4e29cd0137` | `7d980a830aac9d285f572d7a5ab5d0a2f762ab828274b4d0c1a6f3e42832affa` |
| `rei-black` | `05_黑色战斗服/P4-A/selected/idle/frames/00.png` | `e46d9facdf2c6045eed6f031d3fcf8cfffbf434f1ad690a6118e5c5bb3d03455` | `7f39418cc9c11354ad42d6801e480e4a253c862c8bd78c59e2d8780fb49ee8f6` |

---

## 4. 264 格全量离线 QA 实测结果（3 形态 × 88 格）

| 检查项 | 校服 (`rei-school`) | 白服 (`rei-white`) | 黑服 (`rei-black`) | 合计 / 结论 |
| --- | :---: | :---: | :---: | :---: |
| 网格尺寸与模式 (`1536×2288 RGBA`, `8×11`) | PASS | PASS | PASS | **3/3 PASS** |
| 有效格 / 透明空格 (`74 / 14`) | `74 / 14` | `74 / 14` | `74 / 14` | **222 有效 / 42 空格（264/264）** |
| 57 标准帧解码像素与原验收 PNG 一致 | 57/57 | 57/57 | 57/57 | **171/171 逐像素一致** |
| 前九行 57 格与 P4-B 标准图集一致 | PASS | PASS | PASS | **3/3 逐像素一致** |
| 16 方向帧解码像素与 P4-C 验收 PNG 一致 | 16/16 | 16/16 | 16/16 | **48/48 逐像素一致** |
| `R0C6` 与已验收 `idle/00.png` 一致 | PASS | PASS | PASS | **3/3 逐像素一致** |
| 14 空格严格全零 `(0,0,0,0)` | 14/14 | 14/14 | 14/14 | **42/42 全零** |
| Lossless WebP 二进制头 (`VP8L` `0x2f` + Alpha) | PASS | PASS | PASS | **3/3 无损带 Alpha** |
| PNG ↔ WebP 解码往返像素逐字节一致 | PASS | PASS | PASS | **3/3 无损零误差** |
| 全图透明区隐藏 RGB 残留像素 | `0` | `0` | `0` | **0 px** |
| 有效格四周 1 px 透明边框与单一 8 连通主体 | 74/74 | 74/74 | 74/74 | **222/222 PASS** |
| 16 方向无重复像素、无左右/相邻精确镜像 | PASS | PASS | PASS | **3/3 PASS** |
| `rei_atlas_tools.py validate-atlas --require-v2` | EXIT `0` | EXIT `0` | EXIT `0` | **3/3 PASS** |
| `pet.json` v2 契约字段与独立 ZIP 完整性 | PASS | PASS | PASS | **3/3 PASS** |

---

## 5. 上游已验收资产零改动保护证明

装配前后对全部上游受保护资产执行独立 SHA-256 复算，确认 **0 字节修改**：
- 冻结原画与 P2 字节备份：`6/6` 未改动
- 标准化派生母版（含白服 P3-FIX）：`3/3` 未改动
- 已验收标准动作帧：`171/171` 未改动
- 已验收 P4-C 方向帧：`48/48` 未改动（合计 **219/219** 验收帧原字节不变）
- P4-B 标准 `1536×1872` 图集：`3/3` 未改动
- 既有 Windows 本地 Asuka 宠物与原本地开发工作区：全程零接触

---

## 6. 明暗双底 11 行扩展接触表索引

- 校服：[浅底](contact-sheets/rei-school-extended-contact-light.png) · [深底](contact-sheets/rei-school-extended-contact-dark.png)
- 白服 00：[浅底](contact-sheets/rei-white-extended-contact-light.png) · [深底](contact-sheets/rei-white-extended-contact-dark.png)
- 黑服 09：[浅底](contact-sheets/rei-black-extended-contact-light.png) · [深底](contact-sheets/rei-black-extended-contact-dark.png)

---

## 7. 待后续 P5 实机阶段补齐的平台门禁（本轮未执行）

以下项目**未在 P4-D 执行，不得视为已通过**，已完整写入 [WINDOWS_P5_ACCEPTANCE_GUIDE.md](WINDOWS_P5_ACCEPTANCE_GUIDE.md)：
1. Windows 本机 `OpenAI.Codex` MSIX 原生 `validate_atlas.py --require-v2` 对三套最终 `spritesheet.webp` 的平台复检；
2. 经主控与用户授权后，三套独立目录注册、16 方向扇区实机映射、正中心死区实测、任务动画触发观察、完全退出重启持久化、与已安装 Asuka 同尺寸画质对比及安全回退校验。
