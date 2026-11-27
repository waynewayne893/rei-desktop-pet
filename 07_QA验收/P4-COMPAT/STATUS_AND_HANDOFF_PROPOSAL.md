# STATUS_AND_HANDOFF_PROPOSAL.md｜`PROJECT_STATUS.md` 与 `HANDOFF.md` 更新建议

> **说明**：遵循 `REI-PET-CLOUD-BOOTSTRAP`（T4）边界“仅允许本轮新增测试资产与相关文档”，本轮**未直接修改**根目录已冻结文档 [PROJECT_STATUS.md](../../PROJECT_STATUS.md) 与 [HANDOFF.md](../../HANDOFF.md)。以下为待主控验收通过并获用户批准合并至 `main` 后的精确更新建议稿。

---

## 1. 建议更新至 `PROJECT_STATUS.md` 的内容

### 顶部元信息更新建议
- 保留 `唯一正式私有仓库`、`已验证远程资产基线 Commit SHA: 8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`（候选标签 `v0.4.0-p4b-candidate`）与 **`版本定位：P4-B PARTIAL（非正式 v1.0.0）`** 不变。
- 新增一行：
  - `云端接管与预验证分支`：`cloud-bootstrap/p4-compat-preverify`（合并前不覆盖 `main` 基线 `0b430a2d9d52899e8789b21b9fd0d2fbc8f25cea`）。

### 第 1 节“当前真实阶段状态”新增三条状态记录
1. **Linux 云端独立恢复验证（`REI-PET-CLOUD-BOOTSTRAP` T0–T1）**：**`PARTIAL_WITH_EGRESS_NOTE / ASSETS_BYTE_IDENTICAL_PASS`**
   - 在 Antigravity Cloud Linux 容器（`Ubuntu 24.04.5 LTS`, `Python 3.12.16`, 预装 `Pillow 13.0.0` + `libwebp 1.6.0` + `zlib 1.3`）独立复算全部 6 份冻结母版/备份、3 份派生母版、171 帧与 3 套标准图集，全部通过；三套重装标准图集（`/tmp/rei-cloud-check`）与 Windows 提交基线 **100% 像素一致且 PNG SHA-256 逐字节一致**。
   - 同步发现：默认受限网络云端容器阻止访问 `pypi.org`，原版 `06_共用工具/rei_atlas_tools.py` 因缺少 `numpy`/`scipy` 报错（exit `1`）；本次新增纯 Stdlib + Pillow 零外置依赖工具 `06_共用工具/rei_compat_builder.py` 完成全量等价复算。详见 [CLOUD_REPRODUCIBILITY_REPORT.md](../../CLOUD_REPRODUCIBILITY_REPORT.md) 与 [CLOUD_RUNTIME_LOCK.txt](../../CLOUD_RUNTIME_LOCK.txt)。
2. **P4-COMPAT 原生兼容性最小测试包（`rei-compat-test`）**：**`OFFLINE_COMPAT_PASS / PENDING_WINDOWS_USER_TEST`**
   - 仅使用已有 `rei-school` 57 帧 + 16 个带明确角度/方位标识的临时方向测试格 + `(0,6)` 中性参考格 + 14 全透明空格，构建 `1536×2288` RGBA 无损 WebP（`802,834` B，0 透明 RGB 残留，无损往返像素一致）与 v2 `pet.json`，离线校验全部通过；临时方向素材严格隔离于 `07_QA验收/P4-COMPAT/`，不计入正式 P4-C 产物。
   - 已交付可下载包 `rei-compat-test.zip`、哈希清单与 Windows 原生校验/安装/回退指南，等待用户批准后在原 Windows 本机执行 `validate_atlas.py --require-v2` 与浮窗实测。
3. **未授权阶段红线不变**：`P4-B-FIX`、正式 `P4-C`（48 方向帧）、`P4-D`、`P5`、`P6` 均未启动；171 帧原始素材零改动；人工美术终审仍为待完成（仅黑服新版右跑 8 帧 `ACCEPTED`，其余 163 帧 `CANDIDATE`）。

### 第 2 节“下一步任务队列”调整建议
1. **Windows 侧只读执行 `validate_atlas.py --require-v2`** 及（经用户批准后的）`rei-compat-test` 浮窗、16 方向映射、`(0,6)` 中心死区与重启实测，回填 `WINDOWS_COMPAT_TEST_RESULT_TEMPLATE.json` 并安全回退删除临时包。
2. **（可选维护）升级 `06_共用工具/rei_atlas_tools.py`**：增加纯 Pillow 回退路径，消除受限网络云端容器对 `numpy`/`scipy` 的硬依赖。
3. **`REI-PET-REVIEW-CENTER-V1.0`**：开发人工审阅中心完成 171 帧终审。
4. **`REI-PET-P4-B-FIX` → 正式 `P4-C` → `P4-D` → `P5` → `P6`**：等待主控逐阶段授权。

---

## 2. 建议更新至 `HANDOFF.md` 的内容

1. 在第 2 节“云端接续顺序”中，将步骤 1–2 标注为**已完成（含离线 PyPI 沙箱约束记录，云端无 `numpy`/`scipy` 时改用 `06_共用工具/rei_compat_builder.py`）**。
2. 在第 3 节“核心交付文档索引”中新增以下入口：
   - Linux 云端恢复与锁环境报告：[CLOUD_REPRODUCIBILITY_REPORT.md](../../CLOUD_REPRODUCIBILITY_REPORT.md) · [CLOUD_RUNTIME_LOCK.txt](../../CLOUD_RUNTIME_LOCK.txt)
   - 零外置依赖校验与 P4-COMPAT 构建器：[06_共用工具/rei_compat_builder.py](../../06_共用工具/rei_compat_builder.py)
   - P4-COMPAT 临时兼容性测试包与清单：[COMPAT_TEST_MANIFEST.json](COMPAT_TEST_MANIFEST.json) · [COMPAT_OFFLINE_QA.json](COMPAT_OFFLINE_QA.json) · [rei-compat-test.zip](rei-compat-test.zip)
   - Windows 原生验证指南与回填模板：[WINDOWS_COMPAT_TEST_GUIDE.md](WINDOWS_COMPAT_TEST_GUIDE.md) · [WINDOWS_COMPAT_TEST_RESULT_TEMPLATE.json](WINDOWS_COMPAT_TEST_RESULT_TEMPLATE.json)
