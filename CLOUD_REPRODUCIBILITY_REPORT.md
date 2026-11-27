# CLOUD_REPRODUCIBILITY_REPORT.md｜Linux 云端独立恢复与基线复算报告

- **任务编号**：`REI-PET-CLOUD-BOOTSTRAP`（T0–T1）
- **验证日期**：2026-11-27
- **执行环境**：Antigravity Cloud Linux 容器（独立于原 Windows 本地工作区）
- **唯一正式数据源**：`https://github.com/waynewayne893/rei-desktop-pet.git`（已实测 `visibility: PRIVATE`, `isPrivate: true`）
- **当前工程真实阶段**：**`P4-B PARTIAL`**（非正式 `v1.0.0`；171 帧候选仍待人工动态美术终审）

---

## 1. 结论摘要

| 检查项 | 结果 | 实测说明 |
| --- | :---: | --- |
| T0｜远端仓库与基准 HEAD 核验 | **PASS** | `main` 基准 `HEAD = 0b430a2d9d52899e8789b21b9fd0d2fbc8f25cea`，初始资产基线 `8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（tag `v0.4.0-p4b-candidate`），602 文件，无未知远端提交 |
| T1-A｜`pip install -r requirements.txt` 与原版 `rei_atlas_tools.py` | **BLOCKED (Sandbox Egress)** | 当前云端容器外网受限（`pypi.org` 与 Ubuntu `apt` 镜像 DNS 不可解析），容器未预装 `numpy`/`scipy`，原版 `06_共用工具/rei_atlas_tools.py` 报 `ModuleNotFoundError: No module named 'numpy'`（exit `1`） |
| T1-B｜Linux 零外置依赖等价独立验证（纯 Stdlib + 预装 `Pillow 13.0.0`） | **PASS** | 使用容器预装 `Python 3.12.16` + `Pillow 13.0.0`（`libwebp 1.6.0`, `zlib 1.3`）在隔离环境 `.venv` 执行与 `rei_atlas_tools.py` 数学等价的 [06_共用工具/rei_compat_builder.py](06_共用工具/rei_compat_builder.py)：**6/6 冻结母版与备份、3/3 派生母版、171/171 帧、3/3 标准图集全部 `PASS`** |
| T1-C｜Linux 独立重装三套标准图集（像素与 SHA-256 对拍） | **BYTE-IDENTICAL PASS** | 3/3 重装标准图集（`/tmp/rei-cloud-check`）不仅 **`pixel_identical_to_committed = true`**，且 **编码后 PNG SHA-256 与 Windows 基线 100% 逐字节一致（零编码器漂移）** |

> **诚实边界声明**：本次验证证明仓库资产在 Linux 云端可 100% 逐字节恢复与重算，同时也**实测暴露了一个真实云端工程约束**：在默认受限网络（无 PyPI 出网权限）的 Antigravity Cloud 容器中，强依赖 `numpy`/`scipy` 的原版 `06_共用工具/rei_atlas_tools.py` 无法直接运行。因本轮受限于“仅新增测试资产与相关文档”，未修改原版 `rei_atlas_tools.py`，而是新增了零外置依赖（仅用 Stdlib + 预装 Pillow）的 [06_共用工具/rei_compat_builder.py](06_共用工具/rei_compat_builder.py) 完成全量等价复算与 P4-COMPAT 构建。

---

## 2. T0｜云端检出与仓库状态核验

| 字段 | 实测真值 |
| --- | --- |
| 远程仓库 URL | `https://github.com/waynewayne893/rei-desktop-pet.git` |
| 仓库可见性 (`gh repo view`) | `PRIVATE` (`isPrivate: true`, `defaultBranchRef: main`) |
| 检出基准分支 / HEAD | `main` @ `0b430a2d9d52899e8789b21b9fd0d2fbc8f25cea` |
| 初始资产基线 Commit / Tag | `8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8` / `v0.4.0-p4b-candidate` |
| `git fetch origin` 差异检查 | 0 未知远端提交，工作树干净 |
| 基线受控文件数 (`git ls-files`) | `602` |
| 本轮独立任务分支 | `cloud-bootstrap/p4-compat-preverify`（基于 `0b430a2d...` 切出，`main` 未改动） |
| 必读交接文档核读 | `AGENTS.md`、`PROJECT_STATUS.md`、`HANDOFF.md`、`CLOUD_HANDOFF.md`、`CLOUD_ENVIRONMENT.md`、`REPRODUCIBILITY.md`、`07_QA验收/REI_P4B_RESUME_MATRIX.json` |

---

## 3. T1｜实际运行环境与跨平台版本对照

完整锁定记录见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)。

| 组件 | Windows 历史迁移基线 | Linux 云端实测环境 | 备注 |
| --- | --- | --- | --- |
| 操作系统 | `Windows-11-10.0.22000-SP0` | `Ubuntu 24.04.5 LTS` (`Linux 6.18.57 x86_64`, `glibc 2.39`) | 独立云端容器 |
| Python | `3.14.6` | `3.12.16` (`GCC 13.3.0`) | 满足 `>= 3.11` |
| Pillow | `12.3.0` | `13.0.0`（容器预装） | 满足 `>= 11.0.0` |
| libwebp (Pillow 内置) | `1.6.0` | `1.6.0`（系统 `libwebp7 1.3.2-0.4build3`） | 完整支持 RGBA 无损 WebP |
| zlib | `1.3`（CPython/Pillow） | `1.3` | 与 Windows PNG 压缩一致 |
| freetype2 | Windows `consola.ttf` | `2.14.3`（`DejaVuSansMono.ttf` / `DejaVuSans-Bold.ttf`） | 跨平台字体回退正常 |
| NumPy | `2.4.6` | **未安装 (`NOT_INSTALLED`)** | 容器未预装且 `pypi.org` DNS 被沙箱策略拦截 |
| SciPy | `1.18.0` | **未安装 (`NOT_INSTALLED`)** | 容器未预装且 `pypi.org` DNS 被沙箱策略拦截 |

---

## 4. 实测命令与输出证据

### 4.1 隔离环境依赖安装与原版 `rei_atlas_tools.py` 实测（真实阻断留证）

1. 执行 `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`：
   - **退出码**：`1`
   - **实际错误**：`Failed to establish a new connection: [Errno -3] Temporary failure in name resolution`（访问 `/simple/pillow/` 超时重试 5 次失败；`curl -I https://pypi.org/simple/` 返回 `curl: (6) Could not resolve host: pypi.org`；`sudo apt-get update` 亦不可达）。
   - **根因**：Antigravity Cloud 默认非 Turbo 沙箱仅放行已连接插件主机（如 `github.com`），阻止访问公共包源。
2. 改用容器预装环境创建隔离虚拟环境 `python3 -m venv --system-site-packages .venv` 后执行原版脚本：
   - `.venv/bin/python 06_共用工具/rei_atlas_tools.py verify` → **退出码 `1`**，`ModuleNotFoundError: No module named 'numpy'`
   - `.venv/bin/python 06_共用工具/rei_atlas_tools.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets` → **退出码 `1`**，`ModuleNotFoundError: No module named 'numpy'`

### 4.2 Linux 零外置依赖等价独立验证（纯 Stdlib + 预装 `Pillow 13.0.0`）

核查 `06_共用工具/rei_atlas_tools.py` 源码后确认，`numpy` 与 `scipy` 仅用于透明 RGB 清零、边框留白检查、8 连通分量计数与字节对比。新增的 [06_共用工具/rei_compat_builder.py](06_共用工具/rei_compat_builder.py) 使用纯 Python 标准库（含 8 连通 BFS）+ 预装 `Pillow 13.0.0` 实现了 100% 数学等价逻辑：

1. **全量完整性核验**：
   ```bash
   .venv/bin/python 06_共用工具/rei_compat_builder.py verify
   ```
   - **退出码**：`0`
   - **结果**：`"ok": true`
   - `verified_frozen_and_backups`: `6`（三套冻结母版 + `P2_字节备份/` 哈希 6/6 一致）
   - `verified_derived_masters`: `3`（三套 P3 / P3-FIX 派生母版哈希 3/3 一致）
   - `verified_frames`: `171`（全部 171 帧哈希、`192×208 RGBA`、1px 边框透明留白、0 透明隐藏 RGB、单一 8 连通前景主体 171/171 通过）
   - `verified_atlases`: `3`（三套 `1536×1872` 标准图集哈希、57 有效格 + 15 全透明空格、0 透明 RGB 残留 3/3 通过）
   - `errors`: `[]`

2. **独立重新装配与逐像素 / SHA-256 对拍**：
   ```bash
   .venv/bin/python 06_共用工具/rei_compat_builder.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets
   ```
   - **退出码**：`0`
   - **输出文件**（`/tmp/rei-cloud-check`）：3 张重装标准图集 PNG + 3 张接触表 PNG，共 6 文件。

| 形态 | 校验 | 像素一致性 | 原始 RGBA 像素 SHA-256 | 重装文件字节 | 重装 PNG SHA-256 | 与仓库基线 SHA-256 一致 |
| --- | :---: | :---: | --- | ---: | --- | :---: |
| `rei-school` | PASS | **TRUE** | `50cc7e9bcff9f7d95f4bc88513eaea9a279801c631c434ad2d3c694f1f22695e` | `1,076,432` | `59fe359e31ee208d3cd073df0538cf3ee19d029d5a64a37ce591d3ef456ee442` | **TRUE** |
| `rei-white` | PASS | **TRUE** | `23b569b5a58ec7d62fea7ff128e8fac6ac73b89d1f94b9e0ff4dce05e3736458` | `1,108,217` | `8dc945e110fefa5fadb2b9f11b789122cdd785701ccdc5d7a8e3dd18fff4c5ca` | **TRUE** |
| `rei-black` | PASS | **TRUE** | `9121a5a8320b856eb63eaa467d3ff897156deff34d2a46c01cfe51b9c487f00d` | `990,796` | `e7bf03bb0f933a11ec6d3915b924cdf482bb5876368ea48bad6c2119de9ab6c6` | **TRUE** |

### 4.3 跨平台编码器差异分析

- **结论**：本轮 Linux（`Python 3.12.16` + `Pillow 13.0.0` + `zlib 1.3`）与 Windows（`Python 3.14.6` + `Pillow 12.3.0`）重新编码的三套标准 PNG 图集不仅解码 RGBA 像素 100% 相同，**连压缩后 PNG 文件体积与 SHA-256 均 100% 逐字节相同**（`encoder_diff_analysis: null`）。
- **原因**：两端 Pillow 默认 PNG 编码参数（默认压缩级别 6、默认过滤策略、无附加时间戳/文本 chunk）与 `zlib 1.3` 流行为完全一致，证明仓库内标准图集具备跨操作系统逐字节确定性可复现能力。

---

## 5. 后续云端工具链优化建议（待主控授权后执行）

为消除无 PyPI 出网权限云端容器对 `numpy`/`scipy` 的硬阻塞，建议在后续受控维护提交中二选一（或同时采纳）：
1. **推荐方案（零外网依赖）**：批准将 [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py) 升级为“优先使用 `numpy`/`scipy`，未安装时自动回退至纯 Stdlib + Pillow 等价实现”，与 `rei_compat_builder.py` 统一核心内核；
2. **可选配置**：在 Antigravity Cloud 项目网络设置中将 `pypi.org` 与 `files.pythonhosted.org` 加入 `allowed_hosts`（或开启 Turbo 模式）以便 `pip install -r requirements.txt` 安装完整科学计算栈。
