# CLOUD_HANDOFF.md｜Antigravity Cloud 云端接续交付手册

> **架构状态**：GitHub-first + Cloud Execution（本地开发迁移、Linux 云端恢复验证与 Windows 基础兼容性预验证均已结项；GitHub 私有仓库为唯一正式工程数据源）  
> **原生兼容性主控裁定（`REI-P4-COMPAT-MAIN-REVIEW-02`）**：**`BASE_RUNTIME_COMPATIBILITY_PASS`** / **`DETAILED_RUNTIME_VERIFICATION_PARTIAL`**  
> **版本定位**：开发候选基线（**`P4-B PARTIAL`，非正式 `v1.0.0`**）

---

## 1. 仓库与已验证资产基线

| 字段 | 真值 |
| --- | --- |
| 唯一正式远程仓库 | `https://github.com/waynewayne893/rei-desktop-pet.git` |
| 仓库所有者与可见性 | `waynewayne893` / **`PRIVATE`**（严禁公开） |
| 目标分支 | `main` |
| **已验证初始资产基线 Commit SHA** | **`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`** |
| 候选标签 | `v0.4.0-p4b-candidate`（tag 对象 `e18bc9f086014f3c657ae3e4d334a145bc198556`，指向基线提交 `8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`） |
| **兼容性预验证合并基线 Commit SHA** | **`6dc14434c1fcaf82ed1a0f996a6a9142b4f5892d`**（来自已保留分支 `cloud-bootstrap/p4-compat-preverify`，fast-forward 合并至 `main`，原有 602 文件零修改） |
| 历史兼容性证据留存 | `cloud-bootstrap/p4-compat-preverify` 分支及 `07_QA验收/P4-COMPAT/` 完整保留 |

---

## 2. 当前项目真实状态

- **P2**：`PARTIAL`（三套冻结原画与 P2 字节备份锁入基线；历史下载前上游来源继续记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可锁定（含白服 P3-FIX 派生母版、`188 px` 尺度、`(96, 195)` 脚底锚点）。
- **P4-A**：42 帧已齐备并受保护（白服 `idle/attempt-02` 透明修复已锁定；黑服新版 `running-right` 为 `FIX-BLACK` 且已明确人工验收通过 [8 帧]；旧版黑服 `running-right` 为 `REJECTED` 已排除并留档）。
- **P4-B**：**171 帧标准动作候选已齐备**（校服 57 + 白服 57 + 黑服 57），三套 `1536×1872` 标准图集结构校验全部 `STRUCTURE_PASS`；**人工美术验收尚未全部完成**（仅 8 帧 `ACCEPTED`，其余 163 帧仍为 `CANDIDATE`）。
- **Linux 云端恢复验证（已接受）**：在受限外网（无 PyPI）Linux 容器内基于 Python 标准库 + 预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`）完成 171 帧、母版及三套标准图集复算，三套重装标准图集与 Windows 基线 **100% 像素一致且 PNG SHA-256 逐字节一致**（[CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md)）。
- **P4-COMPAT 原生兼容性预验证（已结项）**：主控裁定 **`BASE_RUNTIME_COMPATIBILITY_PASS` / `DETAILED_RUNTIME_VERIFICATION_PARTIAL`**：
  - 临时测试包 `rei-compat-test` 通过 Windows `OpenAI.Codex 26.1120.6357.0` 原生 `validate_atlas.py --require-v2`（退出码 `0`、0 错误、0 警告、88 格逐项一致）；用户亲自实机运行确认无异常；回退后原有 3 套 Asuka 宠物 6 个文件 SHA-256 完全一致。
  - **测试边界**：16 方向逐项映射、`R0C6` 中心死区实际渲染、完全退出重启持久化及任务事件触发动画均未完成逐项实测，留待后续专项验证或 P5 终验，不得标记为已全部通过。
- **P4-B-FIX**：当前暂停——等待人工终审结果及主控裁定透明度替代管线与精确修复清单。
- **正式 P4-C / P4-D / P5 / P6**：**均尚未获得执行授权**，禁止提前启动。

---

## 3. 云端运行环境与工具链约束（实测真值）

- **实测云端容器**：`Ubuntu 24.04.5 LTS`（`Linux 6.18.57 x86_64`）、`Python 3.12.16`、预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`、`freetype2 2.14.3`），详见 [CLOUD_RUNTIME_LOCK.txt](CLOUD_RUNTIME_LOCK.txt)。
- **网络与依赖策略**：Antigravity Cloud 默认受限沙箱无法访问 PyPI（无 `numpy`/`scipy`），且**禁止扩大网络权限或开启 Turbo 模式**。云端核心图像处理统一采用 **Python 标准库 + 预装 Pillow**。
- **验证与装配命令**：
  ```bash
  # 在受限云端环境使用零外置依赖工具（Python stdlib + Pillow）
  python3 06_共用工具/rei_compat_builder.py verify
  python3 06_共用工具/rei_compat_builder.py reassemble --out-dir /tmp/rei-cloud-check --write-sheets
  python3 06_共用工具/rei_compat_builder.py validate-atlas 03_校服绫波丽/P4-B/delivery/spritesheet-standard.png
  ```
  > 注：下一步 `REI-PET-CLOUD-P4B-REVIEW`（T2）将在独立任务分支中统一 `rei_atlas_tools.py` 与 `rei_compat_builder.py` 的单核心入口，并保留历史脚本可追溯性；Windows 原生 `validate_atlas.py --require-v2` 始终保留为最终平台门禁。

---

## 4. 图像生成能力边界（已实测）

- **Antigravity 本地 `image-generator` 实测结论**：**`NATIVE_ALPHA_BLOCKED`**（证据见 [AGY_IMAGE_GEN_CAPABILITY_REPORT.md](07_QA验收/P4-B-FIX/capability-test/AGY_IMAGE_GEN_CAPABILITY_REPORT.md) 与 [agy-image-gen-capability-test.json](07_QA验收/P4-B-FIX/capability-test/agy-image-gen-capability-test.json)）。
- **工程约束**：未获主控正式裁定替代管线前，禁止擅自对不透明生图去背冒充原生透明条带，禁止生成新动画素材。

---

## 5. 待人工验收动作与重点观察项

- **明确人工已验收 (`ACCEPTED`)**：仅黑服新版 `running-right`（**8 帧**，禁止重做）。
- **待人工美术验收 (`CANDIDATE`)**：其余 **163 帧**（26 条动作，含 P4-A 受保护基线 34 帧 + P4-B 新增 129 帧）。
- **离线 QA 重点提示复核的 3 处观察项**：
  1. `rei-school / waiting`（F6 举掌→F1 交握循环切回较直接）
  2. `rei-black / review`（F1–F4 扶臂、F5–F6 垂臂，循环回 F1 姿态切换）
  3. `rei-black / waving`（F1/F4 双臂放松垂放）

---

## 6. 下一阶段云端任务入口（严格分分支、按授权推进）

1. **`REI-PET-CLOUD-P4B-REVIEW`（独立任务分支）**：
   - T2：统一 Stdlib + Pillow 云端工具链入口并复验 171 帧与三套标准图集；
   - T3–T5：开发并实测 `07_QA验收/Review-Center/` 可视化人工验收中心（支持 27 动作统一索引、三形态并排同步、深浅底、1×/2×/4×、严格冻结帧时序、新旧候选对比、00/09 检查、资产哈希绑定防陈旧验收、JSON 导入导出与 Markdown 摘要）并交付离线可用包。
2. **后续排队**：171 帧人工终审 → `REI-PET-P4-B-FIX` → 正式 `P4-C` → `P4-D` → `P5`（回原 Windows 本地安装及细项运行时终验）→ `P6`（均须等待主控逐阶段授权）。

---

## 7. 本地工作区冻结声明

原有 Windows 本地工作区（`D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet`）继续保持冻结：完整保留不删除，停止日常本地开发，仅作历史备份与未来 P5 桌面宠物安装实测环境；明日香参考工程与已安装 3 套明日香宠物继续严格只读保护。
