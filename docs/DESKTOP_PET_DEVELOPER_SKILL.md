# Desktop Pet Developer V1.0｜桌面宠物开发技能

Portable, generic workflow for building a Codex Desktop Pets–compatible sprite pet from a user-approved art master. This document is the engineering-repo copy of the private Grok Bot skill of the same name. It is **not** a character bible and must not hard-code any one character’s identity, costume, display height, foot anchor, or branch name.

本文件是通用开发规范的可移植副本，与任一具体角色任务的参数分离。角色专用数值（显示高度、锚点、服装、Pet ID、工作分支等）只写在该项目自己的状态与冻结清单中。

- **Version / 版本**：V1.0
- **Art baseline repo / 美术基线仓库**：<https://github.com/waynewayne893/asuka-desktop-pet>
- **Engineering baseline repo / 工程基线仓库**：<https://github.com/waynewayne893/rei-desktop-pet>
- **Source of truth / 正式数据源**：GitHub. At the start of every task, read the actual default branch, project status, `AGENTS.md`, technical specs, and the latest *valid* delivery record. Do not reuse stale phase labels from old reports, and do not re-explore capabilities already verified in those records.

Successful runs may suggest skill improvements; **do not overwrite a verified rule without explicit review**. Do not create unsolicited automation routines, and do not perform a formal public release without authorization.

---

## Inputs / 技能输入

For a new pet the owner should supply, in principle, only:

1. Character name.
2. An already approved art master.
3. Costume or style requirements.
4. Target runtime platform.
5. Optional special actions or mechanics.

Everything else is inherited from the baseline repositories first. Do not rebuild a general atlas toolkit, and do not overwrite historical assets.

---

## S1 — Reuse matrix / 工程复用

Read the art and engineering baseline repositories. Classify each item:

| Class | Meaning / 含义 |
| --- | --- |
| **A** | Direct reuse / 直接复用 already-verified tools, grid protocol, QA method, `pet.json` field template. |
| **B** | Parameterized adaptation / 参数化适配 (paths, pet ID, display height, foot anchor, packing entry points). |
| **C** | Character-specific design / 角色独立设计 (acting, costume motion, expressions, laterality, gaze). |
| **D** | Do not migrate / 禁止迁移 (other characters’ pixels and IDs, private user data, restricted runtime components such as bundled `hatch-pet` scripts, unverified redistribution rights). |

Never invent a second copy of a verified atlas tool when the baseline already has one.

---

## S2 — Art master freeze / 美术母版冻结

1. Store the owner-approved original master **unchanged**, with SHA-256.
2. Inspect real alpha (do not describe a cutout of an opaque image as native-alpha generation), hidden RGB under `alpha = 0`, edge fringe / halo, and silhouette completeness.
3. Produce a derived RGBA master (document every pixel change, e.g. clearing `alpha < 8`) and a native-size cell preview on **light and dark** backgrounds.
4. Display height and foot anchor are **per-master**. Adapt them to the new master and, when a related pet already exists, compare against its actual on-screen size. Do not hard-code one height/anchor for every future character.
5. Stop for **owner art approval**. No full-motion production until the static master is frozen.

---

## Art production modes / 美术生产方式

This skill formally supports two art-production modes. External art input is a first-class, supported mode — **not** a temporary exception.

本技能正式支持两种美术生产方式。外部美术资产输入是一等正式模式，不是临时例外。

### 1. External art input mode / 外部美术资产输入模式

Formally supported, and the **default** for copyrighted or third-party characters.

An external tool the owner runs (for example Codex image generation) produces the real motion frames. The assistant owns intake, normalization, QA, animated and native-size previews, atlas assembly, delivery packaging, and GitHub persistence. It prepares an intake environment — per-state frame folders, naming rules, `_incoming` drop folders, a QA script, a manual review template, and an intake document — and **waits for frames**. It does not generate new artwork of those characters.

对受版权保护或第三方角色，默认采用此模式：由用户运行的外部工具（例如 Codex 生图）产出真实动作帧；助手负责资产接收、标准化、QA、动画与原生尺寸预览、图集装配、交付打包与 GitHub 持久化。助手先准备接收环境，然后等待交帧。

### 2. Self-generation mode / 自主生图模式

Available **for original characters only**. When tools allow, the assistant may generate motion frames itself, still under the frozen-master constraint and the common frame-source rules in S3.

仅适用于原创角色。在工具能力允许时，助手可自行生成动作帧，仍须遵守已冻结母版约束及 S3 的共同规则。

---

## S3 — Frame source / 帧来源

Select the mode under “Art production modes / 美术生产方式” first. The following rules apply no matter which tool produced the frames:

无论由哪种工具出帧，均须遵守：

- Never pass off simple scale, rotation, or other affine warps as real character acting. / 不得用简单缩放、旋转或其他仿射变换冒充真实人物动作。
- Record whether each asset has a native alpha channel or is a cutout of an opaque render. A cutout must be labelled as such, never as native-alpha generation. / 必须记录原生透明通道与后期去背的区别，不得把不透明图去背结果称为原生 Alpha 生图。
- Keep the raw images and the production prompts from whichever tool produced them. / 保留原始生成图片及提示词，不论它们出自何种工具。
- If a required frame source or tool is unavailable, report the concrete blocker; **never fabricate frames**. / 如存在能力或来源阻塞，报告具体阻塞项，不得伪造生成结果。
- Unverified redistribution rights imply private or controlled storage — public visibility is not an open-source or redistribution licence. / 未核实再分发权利的资产使用私有或受控存储；公开可见不等于开源或再分发许可。

In self-generation mode, also check available image-generation tools, reference-image control, output format, and whether a true alpha channel is produced. Prefer real generated action strips under a frozen-master constraint. If a Teach a task demonstration is required, state the minimum steps to record.

自主生图模式下，另须检查可用生图工具、参考图控制、输出格式及是否产生真实透明通道；优先生成连续动作条带。如需 Teach a task 演示，应给出最小教学步骤。

---

## S4 — Core-action pilot / 核心动作试生产

Produce only the first batch, then stop for owner review:

- `idle`：6 frames
- `running-right`：8 frames

Deliver a real animation preview and a native-size preview. Check appearance consistency with the frozen master, motion continuity, transparent edges, foot-anchor stability, and body proportions. Do not expand to other states until the owner accepts this batch. Already accepted frames must not be regenerated without cause.

---

## S5 — Full animation / 完整动画生产

Inherit the verified nine-state protocol (57 standard frames), then 16 directional look-at frames:

| State | Frames |
| --- | ---: |
| `idle` | 6 |
| `running-right` | 8 |
| `running-left` | 8 |
| `waving` | 4 |
| `jumping` | 5 |
| `failed` | 8 |
| `waiting` | 6 |
| `running` | 6 |
| `review` | 6 |

Left/right semantics must be correct. Do not regenerate accepted assets without a recorded reason.

---

## S6 — Atlas assembly / 标准图集装配

Use the Rei-verified v2 protocol as the **initial** baseline, and **re-verify against the current runtime** before packing:

| Item / 项 | Baseline / 基准（须先用当前运行端核对） |
| --- | --- |
| Cell / 单格 | 192×208 RGBA |
| Standard atlas / 标准图集 | 1536×1872（8×9） |
| Extended atlas / 扩展图集 | 1536×2288（8×11） |
| Occupancy / 占用 | 57 standard + 16 look-at + 1 R0C6 neutral reference + 14 fully transparent blanks = **88** cells |

Character display height and foot anchor remain per-master (see S2). Do not copy or redistribute restricted runtime components. Install under a **new unique pet ID**; never overwrite an existing pet.

---

## S7 — Quality acceptance / 质量验收

Run all of the following, and keep the three verdicts separate:

- Transparent background and edge checks (including hidden RGB and fringe).
- Inter-frame proportion / scale consistency.
- Crop and cell-overflow checks.
- Motion continuity.
- Look-at direction semantics.
- Atlas structure validation.
- SHA-256 integrity.
- Owner art review.
- Native desktop-pet runtime test.

**A script pass is not an art pass. An offline QA pass is not a runtime pass.** Unrun live tests must not be marked `PASS`.

---

## S8 — Delivery and archive / 交付与归档

Expected outputs:

- `spritesheet.webp`
- `pet.json`
- Standalone install ZIP
- `SHA256SUMS`
- Necessary art masters and accepted frames
- Animation previews
- QA reports
- Production prompts (when generation was used)
- Project status and handoff notes

Respect repository permissions and release authorization. Propose local workspace cleanup **only after** an independent download-and-restore test has passed. Do not delete local files without authorization.

---

## Maintenance / 维护

- Keep this generic skill and each project’s parameters in **separate** documents.
- After a successful project, improvements may be proposed; apply them only after they have been verified.
- This file lives in the engineering baseline so the workflow does not exist only inside a single assistant’s memory.
