# REI-PET-P4B-FIX｜Antigravity `image-generator` 最小能力验证报告

**验证结论：`NATIVE_ALPHA_BLOCKED`（角色身份与动作语义生成能力优秀，但原生透明通道与 3:1 画幅存在硬性工具缺口；按移交规范立即停止并上报主控裁定替代方案，未触碰任何已有 P4-B 交付资产）。**

---

## 1. 最小验证任务与输入

- **测试对象**：`rei-school / waiting`（6 帧，验证闭环收手动作）
- **参考输入**：
  - 冻结派生母版：`02_标准化母版/rei-school/master-rgba.png`
  - 既有条带参考：`03_校服绫波丽/P4-B/originals/waiting/attempt-01/source.png`
- **执行工具**：Antigravity 原生 `image-generator`（`generate_image`），共 3 次尝试，全部原样归档于 `07_QA验收/P4-B-FIX/capability-test/`，原始 JSON 见 [agy-image-gen-capability-test.json](agy-image-gen-capability-test.json)。

---

## 2. 实测样本与 `hatch-pet` 门禁结果

| 样本 | 格式 / 尺寸 / 模式 | SHA-256 | `load_native_alpha_image` | 视觉实查 |
| --- | --- | --- | :---: | --- |
| [test_01.jpg](rei_school_waiting_agy_test_01_1795784314464.jpg) | JPEG / 1376×768 / RGB | `78f6c177970e7e12bedd56b97ae283645604844c82f60445d6a75fa3efc68d16` | **FAIL**（无 Alpha 通道） | 要求透明时被烤入灰白棋盘格背景；6 姿身份极高、左手抬掌一致、F6 收手闭环 |
| [test_02.jpg](rei_school_waiting_agy_test_02_1795784339012.jpg) | JPEG / 1376×768 / RGB | `e7da7a9efd5e211942a2c4a9e72954dfc7cff2f045afaa57fcec3aa5ae3caa95` | **FAIL**（无 Alpha 通道） | 纯白 `#FFFFFF` 背景干净；6 姿身份与线稿高度一致、F4 半眨眼 F5 闭眼 F6 闭环；16:9 宽度紧张致 F5–F6 发梢轻微相触，且 F3/F4 抬手换侧 |
| [test_03.jpg](rei_school_waiting_agy_test_03_1795784361763.jpg) | JPEG / 1376×768 / RGB | `fa789ea0fdb7c91c5a8adc2d7eae8a8070edc808a575d30a6affb4e1fd42cb0c` | **FAIL**（无 Alpha 通道） | 纯白 `#FFFFFF` 背景干净、手臂一致；因 16:9 间距放宽导致仅生成 5 姿（缺 1 帧） |

`hatch-pet/scripts/extract_strip_frames.py` 返回的精确门禁错误（3/3 相同）：
`has no encoded alpha channel; preserve the original and request approval for a replacement with transparent_background: true`

---

## 3. 能力评估与硬性缺口

### 已通过项
- **角色身份与画风继承（PASS）**：发色、呆毛、白发夹、红瞳、红领结、百褶裙、白袜白鞋、Q 版头身比及线稿粗细与 `master-rgba.png` 高度一致。
- **动作语义与闭环（PASS）**：可按指令生成连续姿态、眨眼与首尾闭环。

### 阻断性工具缺口
1. **无原生 RGBA 透明输出（BLOCKING）**：Antigravity `generate_image` 仅输出不透明 RGB `.jpg`，无 `transparent_background: true` 参数。按原 `hatch-pet/SKILL.md:35` 及 P4 合同，禁止擅自对不透明背景做本地抠图/补 Alpha 后冒充原生透明条带，必须上报主控授权替代管线。
2. **无 3:1 横向条带比例（LAYOUT CONSTRAINT）**：`generate_image` 最宽仅支持 `16:9`（`1376×768`），单行排布 6–8 姿易发生发梢粘连或漏帧。

---

## 4. 供 ChatGPT 主控裁定的可行替代方案

- **方案 A（推荐｜Antigravity 纯本地闭环）**：
  1. 获准对 Antigravity 新生成的动作采用 **纯色色键底（如洋红 `#FF00FF` 或纯绿 `#00FF00`，避开校服/白服/黑服全身色域）** 生成；
  2. 采用 **2×3 / 2×4 网格或分批 1×4 条带** 规避 `16:9` 横向拥挤（彻底消除发梢粘连）；
  3. 经确定性色键抠图 + 随附 `hatch-pet/scripts/despill_chroma_edges.py` 脱溢色 + P3 同级明暗双底边缘/零彩边/零隐藏 RGB 验收后，送入既有 `build_rows.py` 与 `assemble_delivery.py`。
- **方案 B（仅当坚持原生 RGBA 生成）**：由主控/用户接入支持原生 `transparent_background` PNG 的外部生图通道，由 Antigravity 负责本地工程分帧、注册、装配与 QA。

---

## 5. 待主控同时明确的两项裁定

1. **透明度管线裁定**：是否批准 **方案 A（纯色色键底 + 网格布局 + 确定性抠图与 `despill_chroma_edges.py` 严格明暗底 QA）** 作为 Antigravity 阶段（P4-B-FIX 及 P4-C）的新生成素材合规标准？
2. **`REI-PET-P4-B-FIX` 精确修复清单**：请明确本轮 `P4-B-FIX` 具体需重制的动作列表（例如：是否仅修复此前 QA 标出的 3 项观察项 `rei-school / waiting`、`rei-black / review`、`rei-black / waving`，或包含其他人工验收指定动作）？
