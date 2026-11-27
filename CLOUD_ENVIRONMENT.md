# CLOUD_ENVIRONMENT.md｜Antigravity Cloud 云端开发环境与工具链说明

本项目自 `REI-PET-GIT-CLOUD-MIGRATION` 起正式由 Local-first 切换为 **GitHub-first + Cloud Execution**，并已通过 `REI-PET-CLOUD-BOOTSTRAP` 的 Linux 云端独立恢复验证及 `REI-P4-COMPAT-MAIN-REVIEW-02` 的基础原生兼容性裁定（`BASE_RUNTIME_COMPATIBILITY_PASS` / `DETAILED_RUNTIME_VERIFICATION_PARTIAL`）。

---

## 1. 云端实测运行环境基线（已锁定）

完整锁定文件见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)，实测复算报告见 [CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md)：

- **操作系统**：`Ubuntu 24.04.5 LTS`（`Linux 6.18.57 x86_64`, `glibc 2.39`）
- **Python 版本**：`Python 3.12.16`（兼容 `Python >= 3.11`；Windows 历史基线为 `Python 3.14.6`）
- **核心图像处理依赖（唯一云端必需外部包）**：
  - `pillow==13.0.0`（容器预装，内置 `libwebp 1.6.0`、`zlib 1.3`、`freetype2 2.14.3`、`libjpeg_turbo 3.2.0`）
- **沙箱网络边界（实测）**：
  - Antigravity Cloud 默认非 Turbo 容器仅放行已连接插件主机（如 `github.com`），无法访问 `pypi.org` 或 Ubuntu `apt` 镜像；
  - 容器未预装 `numpy` / `scipy`；**工程规则明确不扩大云端网络权限、不开启 Turbo 模式**，云端核心图像处理统一采用 **Python 标准库 + 预装 Pillow**。

---

## 2. 跨平台工具链架构与原 Windows 组件处理

### 2.1 云端洁净工具链
- [06_共用工具/rei_compat_builder.py](06_共用工具/rei_compat_builder.py)：零外置依赖（仅 Python 标准库 + Pillow）独立实现的校验、三套标准图集重装及 P4-COMPAT v2 扩展图集构建工具；已在受限云端容器内完成 171 帧核验、三套标准图集逐字节重装与 `rei-compat-test` v2 无损 WebP 构建，且 88 格离线 QA 与 Windows 原生 `validate_atlas.py --require-v2` 逐项一致。
- [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py)：初始跨平台校验/重装脚本（历史依赖 `numpy`/`scipy`，在无 PyPI 容器内无法直接运行；后续 `REI-PET-CLOUD-P4B-REVIEW` T2 将在独立任务分支中以 Stdlib + Pillow 统一工具入口并保留历史可追溯性）。
- 内置跨平台字体回退（Linux `DejaVuSansMono`/`DejaVuSans-Bold`/`LiberationMono` → macOS `Menlo` → Windows `consola.ttf` → Pillow 内置字体）。

### 2.2 受限专有组件与最终平台门禁：`OpenAI.Codex` 随附 `hatch-pet`
- **许可与隔离边界**：原 Windows 工程依赖 `C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0\app\resources\skills\skills\.curated\hatch-pet\scripts\*`，属于专有桌面应用内置组件，**严禁复制或上传至本仓库**。
- **最终平台门禁**：Windows 原生 `validate_atlas.py --require-v2` 始终保留为最终平台门禁；在 `P4-COMPAT` 预验证中已由原 Windows 环境实测通过（退出码 `0`、0 错误、0 警告，详见 [WINDOWS_NATIVE_VALIDATION_V2.json](07_QA验收/P4-COMPAT/WINDOWS_NATIVE_VALIDATION_V2.json)）。
- 历史 Codex 阶段脚本（`build_static_masters.py`、`build_p3_fix.py`、`build_preview_row.py`、`build_rows.py`、`assemble_delivery.py`）按原字节留档供审计追溯。

---

## 3. 图像生成能力边界（已实测）

详见实测报告 [07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md)：
- Antigravity `image-generator` 实测为 **`NATIVE_ALPHA_BLOCKED`**（仅输出不透明 RGB JPEG、最大 `16:9`）；
- 未获主控对替代管线的正式授权前，禁止生成新素材或用去背冒充原生透明条带。

---

## 4. 云端与 Windows 环境分工边界

| 阶段 | 云端可执行 | 仍需原 Windows 环境 |
| --- | :---: | :---: |
| 资产哈希核验、图集重装、结构校验、接触表/WebP 编码、Review Center 构建 | **是（已验证）** | 可选 |
| P4-B 171 帧人工动态美术审阅（通过 Review Center 离线包） | **云端产出离线包** | 用户本地浏览器双击审阅 |
| P4-B-FIX / 正式 P4-C 新素材生成（待主控裁定透明度方案后） | **是（待授权）** | 否 |
| P4-D 扩展图集 `1536×2288` WebP 装配与离线结构校验 | **是（已预验证架构）** | 原生 `validate_atlas.py --require-v2` 最终门禁 |
| P5 本地 Codex Desktop Pets 注册、16 方向/`R0C6`/任务事件/重启终验 | 否 | **必须（仅本地 Windows）** |
