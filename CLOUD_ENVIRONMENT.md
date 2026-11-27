# CLOUD_ENVIRONMENT.md｜Antigravity Cloud 云端开发环境与工具链说明

本项目自 `REI-PET-GIT-CLOUD-MIGRATION` 起正式由 Local-first 切换为 **GitHub-first + Cloud Execution**。GitHub 私有仓库 `https://github.com/waynewayne893/rei-desktop-pet.git` 为唯一正式工程数据源，Windows 本地工作区仅保留为历史备份与最终桌面宠物安装测试环境。

---

## 1. 云端运行环境基线（Linux / macOS / Windows 通用）

- **操作系统**：支持标准 Linux 云端容器（Antigravity Cloud）、macOS 与 Windows。
- **Python 版本**：推荐 Python `3.11+`（已验证基线：`Python 3.14.6`）。
- **核心依赖（详见 [requirements.txt](requirements.txt)）**：
  - `Pillow>=11.0.0`（含 `libwebp` 支持，用于 RGBA PNG/WebP 编解码及 GIF 预览）
  - `numpy>=2.0.0`（像素级 Alpha 通道、边框留白与零隐藏 RGB 校验）
  - `scipy>=1.14.0`（8 连通前景主体检测）
- **云端初始化命令**：
  ```bash
  git clone https://github.com/waynewayne893/rei-desktop-pet.git
  cd rei-desktop-pet
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python3 06_共用工具/rei_atlas_tools.py verify
  ```

---

## 2. 跨平台工具链架构与原 Windows 组件处理

### 2.1 可直接在云端独立运行的洁净跨平台工具
- 仓库内新增完全独立编写的跨平台工具：[06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py)
  - 仅使用标准库 + `Pillow`/`NumPy`/`SciPy` + `pathlib.Path` 相对路径；
  - 支持 `--root <repo_path>` 可配置项目根目录；
  - 内置跨平台字体回退（Linux `DejaVuSansMono`/`LiberationMono`/`NotoSansMono` → macOS `Menlo` → Windows `consola.ttf` → Pillow 内置字体）；
  - 覆盖 171 帧与冻结母版哈希校验 (`verify`)、标准/v2 扩展图集独立结构校验 (`validate-atlas`)、三套 `1536×1872` 标准图集独立重装与逐像素一致性比对 (`reassemble`)。

### 2.2 无法合法随仓库迁移的受限组件：`OpenAI.Codex` 随附 `hatch-pet`
- **来源与许可状态**：原 Windows 工程依赖 `C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0\app\resources\skills\skills\.curated\hatch-pet\scripts\*`。经只读核查，该 MSIX 安装包内未提供开源再分发许可证，属于专有桌面应用内置组件，**严禁复制或打包上传至本仓库**。
- **云端替代方案**：
  - 云端日常生产、结构校验与图集装配使用 [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py)（基于本仓库公开记录的 192×208 / 8×9 / 8×11 协议独立实现，零代码拷贝）。
  - 历史 Codex 阶段脚本（`02_标准化母版/build_static_masters.py`、`02_标准化母版/P3-FIX/build_p3_fix.py`、`07_QA验收/P4-A/build_preview_row.py`、`07_QA验收/P4-B/build_rows.py`、`07_QA验收/P4-B/assemble_delivery.py`）作为历史复算证据原样保留；在 Linux 云端如需运行 `build_preview_row.py`/`assemble_delivery.py`，因其硬编码 `C:/Windows/Fonts/consola.ttf` 并引用 `hatch-pet`，请改用 `06_共用工具/rei_atlas_tools.py`。
- **最终 P5 阶段 Windows 端复核**：仅在 P5 本地安装验收前，于已安装 Windows `OpenAI.Codex` 的本地机器上只读调用官方 `validate_atlas.py --require-v2` 做最终双校验，并安装至 `C:\Users\<user>\.codex\pets\` 测试实际浮窗运行。

---

## 3. 图像生成能力边界（已实测）

详见实测报告 [07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)：

- **已验证强项**：Antigravity `image-generator` 引用冻结/派生母版时，角色身份、服装细节、比例与线稿还原度极高。
- **已知阻断缺口 (`NATIVE_ALPHA_BLOCKED`)**：
  1. `generate_image` 仅输出不透明 RGB JPEG（无 `transparent_background: true` 参数）；
  2. 最大宽屏比例为 `16:9`（无 `3:1` 条带）。
- **待主控裁定**：在执行任何需要全新生图的任务（`P4-B-FIX` 局部重制或 `P4-C` 16 方向注视）前，必须先获得主控对替代管线（方案 A：纯色色键底 + 2×3/2×4 网格 + 确定性抠图与明暗双底严检；或方案 B：接入原生 RGBA 通道）的正式授权。

---

## 4. 仍需原 Windows 环境的步骤边界

| 阶段 | 云端可执行 | 仍需原 Windows 环境 |
| --- | :---: | :---: |
| 资产哈希核验、图集重装、结构校验、接触表/GIF 生成 | **是** | 可选 |
| P4-B-FIX / P4-C 新素材生成（待主控裁定方案后）与 QA 审阅页 | **是** | 否 |
| P4-D 扩展图集 `1536×2288` PNG/WebP 装配与独立结构校验 | **是** | 仅最终官方 `validate_atlas.py --require-v2` 双验 |
| P5 本地 Codex Desktop Pets 注册、浮窗实测与重启验收 | 否 | **必须（仅本地 Windows）** |
