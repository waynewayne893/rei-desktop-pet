# CLOUD_HANDOFF.md｜Antigravity Cloud 云端接续交付手册

> **架构状态**：GitHub-first + Cloud Execution（本地开发迁移、Linux 云端恢复验证与 Windows 基础兼容性预验证均已结项；GitHub 私有仓库为唯一正式工程数据源）  
> **原生兼容性主控裁定（`REI-P4-COMPAT-MAIN-REVIEW-02`）**：**`BASE_RUNTIME_COMPATIBILITY_PASS`** / **`DETAILED_RUNTIME_VERIFICATION_PARTIAL`**  
> **版本定位**：`P4-D_CANDIDATE_OFFLINE_QA_PASS`，待主控独立验收及 P5 授权（尚未正式发布 `v1.0.0`）

---

## 1. 仓库与已验证资产基线

| 字段 | 真值 |
| --- | --- |
| 唯一正式远程仓库 | `https://github.com/waynewayne893/rei-desktop-pet.git` |
| 仓库所有者与可见性 | `waynewayne893` / **`PRIVATE`**（严禁公开） |
| 目标分支 | `main` |
| **已验证初始资产基线 Commit SHA** | **`8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`** |
| 候选标签 | `v0.4.0-p4b-candidate`（tag 对象 `e18bc9f086014f3c657ae3e4d334a145bc198556`，指向基线提交 `8e5f592d8f93fd6a0b5485462e3e2a7591b57fd8`） |
| **兼容性预验证分支 Commit SHA** | **`6dc14434c1fcaf82ed1a0f996a6a9142b4f5892d`**（来自已保留分支 `cloud-bootstrap/p4-compat-preverify`，是专项试验分支的祖先。结项核验时远端 `main` 仍在 `0b430a2`） |
| 历史兼容性证据留存 | `cloud-bootstrap/p4-compat-preverify` 分支及 `07_QA验收/P4-COMPAT/` 完整保留 |

---

## 2. 当前项目真实状态

- **P2**：`PARTIAL`（三套冻结原画与 P2 字节备份锁入基线；历史下载前上游来源继续记为缺失）。
- **P3 / P3-FIX**：生产输入已获用户认可锁定（含白服 P3-FIX 派生母版、`188 px` 尺度、`(96, 195)` 脚底锚点）。
- **P4-A**：42 帧已齐备并受保护（白服 `idle/attempt-02` 透明修复已锁定；黑服新版 `running-right` 为 `FIX-BLACK` 且已明确人工验收通过 [8 帧]；旧版黑服 `running-right` 为 `REJECTED` 已排除并留档）。
- **P4-B**：171 帧通过结构检查，正式 27/27 动作、171/171 帧完成人工验收，三个标准图集保持原字节。 [验收台账](07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json)
- **Linux 云端恢复验证（已接受）**：在受限外网（无 PyPI）Linux 容器内基于 Python 标准库 + 预装 `Pillow 13.0.0`（`libwebp 1.6.0`、`zlib 1.3`）完成 171 帧、母版及三套标准图集复算，三套重装标准图集与 Windows 基线 **100% 像素一致且 PNG SHA-256 逐字节一致**（[CLOUD_REPRODUCIBILITY_REPORT.md](CLOUD_REPRODUCIBILITY_REPORT.md)）。
- **P4-COMPAT 原生兼容性预验证（已结项）**：主控裁定 **`BASE_RUNTIME_COMPATIBILITY_PASS` / `DETAILED_RUNTIME_VERIFICATION_PARTIAL`**：
  - 临时测试包 `rei-compat-test` 通过 Windows `OpenAI.Codex 26.1120.6357.0` 原生 `validate_atlas.py --require-v2`（退出码 `0`、0 错误、0 警告、88 格逐项一致）；用户亲自实机运行确认无异常；回退后原有 3 套 Asuka 宠物 6 个文件 SHA-256 完全一致。
  - **测试边界**：16 方向逐项映射、`R0C6` 中心死区实际渲染、完全退出重启持久化及任务事件触发动画均未完成逐项实测，留待后续专项验证或 P5 终验，不得标记为已全部通过。
- **P4-C**：48/48 方向帧通过结构与 12/12 主方向盲检，并经用户明确确认全部人工验收通过（原始 7+41 JSON 原样归档，41 帧补充验收单独登记，219 帧全部保持原字节）。[P4-C 验收台账](07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json)
- **最新主控裁定**：`CODEX_CLOUD_ART_PIPELINE_QUALIFIED`、`P4-B-FIX_SKIPPED`、`P4-C_ART_ACCEPTANCE_PASS`、`P4-D_FINAL_ASSEMBLY_AUTHORIZED`。全部美术生产已完成，P4-D 无需调用生图；P5、P6 仍待逐阶段授权。

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
- **工程约束**：正式 P4-C 使用已验证的 Codex Cloud 原生 RGBA 路径，按专项试验的 Alpha 门禁及失败记录要求逐批检查。

---

## 5. 人工验收结果

- **P4-B 正式标准动作**：27/27 动作、171/171 帧全部 `ACCEPTED`（试验 waiting 6 帧作为通过的备用候选，正式图集沿用原版）。[P4-B 验收台账](07_QA验收/P4-B/human-acceptance/ACCEPTANCE_LEDGER.json)
- **P4-C 16 方向注视**：3 形态 48/48 帧全部 `ACCEPTED`（原始 7 `ACCEPTED` + 41 `PENDING_HUMAN_REVIEW` JSON 原样归档，结合用户明确确认「48个方向全部人工验收通过」单独登记 41 帧 `ACCEPTED`）。[P4-C 验收台账](07_QA验收/P4-C/human-acceptance/P4C_ACCEPTANCE_LEDGER.json)

## 6. 下一阶段任务入口

`main` 已于 `44624e1572894f340e9b334ab339d958e7fb9ba2` 完成 P4-C 结项统一；`feat/p4d-final-assembly` 已完成三套 v2 扩展图集装配、264 格离线 QA（[P4D_QA_REPORT.md](07_QA验收/P4-D/P4D_QA_REPORT.md)）、独立与总交付包（[P4D_DELIVERY_MANIFEST.json](08_正式交付/P4-D-candidate/P4D_DELIVERY_MANIFEST.json)）及 Windows P5 验收指南（[WINDOWS_P5_ACCEPTANCE_GUIDE.md](07_QA验收/P4-D/WINDOWS_P5_ACCEPTANCE_GUIDE.md)）。等待主控对 P4-D 独立验收后授权进入 Windows P5 实机验收。

---

## 7. 本地工作区冻结声明

原有 Windows 本地工作区（`D:\HuaweiMoveData\Users\86191\Desktop\Rei Desktop Pet`）继续保持冻结：完整保留不删除，停止日常本地开发，仅作历史备份与未来 P5 桌面宠物安装实测环境；明日香参考工程与已安装 3 套明日香宠物继续严格只读保护。
