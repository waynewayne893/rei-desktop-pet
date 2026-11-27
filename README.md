# Rei Desktop Pet（绫波丽桌面宠物 V1.0 工程仓库）

> **架构模式**：GitHub-first + Cloud Execution（本 GitHub 私有仓库为唯一正式工程数据源；原 Windows 本地工作区仅保留为历史备份及最终 P5 安装测试环境）  
> **当前阶段**：`P4-B_ART_ACCEPTANCE_PASS`（27/27 动作、171/171 帧人工通过，P4-C 已获授权；尚未正式发布）
> **仓库可见性**：`Private`（禁止公开） ｜ **项目主控**：ChatGPT ｜ **执行器**：Antigravity Cloud / Local

---

## 1. 三套独立产品概览

本项目面向 Codex Desktop Pets v2 协议，独立开发三套绫波丽桌面宠物（不做形态热切换）：

| 产品 ID | 角色形态 | 冻结原画母版 | 标准化派生母版 | 当前 1536×1872 标准图集 |
| --- | --- | --- | --- | --- |
| `rei-school` | 校服绫波丽 | `00_原始美术母版/rei-school-base-v1.0.png` | `02_标准化母版/rei-school/master-rgba.png` | 57/57 帧 `ACCEPTED` |
| `rei-white` | 白色战斗服绫波丽（`00`） | `00_原始美术母版/rei-white-base-v1.0.png` | `02_标准化母版/P3-FIX/rei-white-master-rgba-p3-fix.png` | 57/57 帧 `ACCEPTED` |
| `rei-black` | 黑色战斗服绫波丽（`09`） | `00_原始美术母版/rei-black-base-v1.0.png` | `02_标准化母版/rei-black/master-rgba.png` | 57/57 帧 `ACCEPTED` |

---

## 2. 冻结规范摘要

- **单帧几何**：`192×208` RGBA 透明背景，`188 px` 中性人物实体高，`(96, 195)` 脚底锚点，严格等比例缩放。
- **标准九状态（57 帧 / 套，三套共 171 帧）**：`idle`(6)、`running-right`(8)、`running-left`(8)、`waving`(4)、`jumping`(5)、`failed`(8)、`waiting`(6)、`running`(6)、`review`(6)。
- **目标 v2 扩展图集（P4-D 待授权）**：`1536×2288`（8×11，57 标准动作 + 16 方向注视 + `(0,6)` 中性格 = 74 有效格 + 14 全透明格）。

---

## 3. 统一 Agent 接续入口（新会话必读）

| 入口文件 | 作用 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 跨 Agent 执行规则、工程隔离红线与工具边界 |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | 真实阶段状态、171 帧与哈希真值、当前阻塞项 |
| [HANDOFF.md](HANDOFF.md) | 当前断点与下一步授权动作清单 |
| [CLOUD_ENVIRONMENT.md](CLOUD_ENVIRONMENT.md) | 云端环境初始化、跨平台工具链与 Windows 边界说明 |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | 干净环境恢复、全量哈希核验与标准图集独立重装指南 |
| [requirements.txt](requirements.txt) | 跨平台 Python 依赖清单 |
| [GIT_CLOUD_MIGRATION_PREFLIGHT.md](GIT_CLOUD_MIGRATION_PREFLIGHT.md) | GitHub 云端迁移首次提交预审报告 |
| [06_共用工具/rei_atlas_tools.py](06_共用工具/rei_atlas_tools.py) | 洁净跨平台（Linux/macOS/Windows）校验与标准图集重装工具 |
