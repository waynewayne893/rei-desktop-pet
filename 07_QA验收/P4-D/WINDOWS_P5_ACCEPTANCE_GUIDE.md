# WINDOWS_P5_ACCEPTANCE_GUIDE.md｜Windows Codex Desktop Pets v2 正式三形态 P5 安装与运行验收指南

> **强制治理门禁声明**：
> 1. 本指南对应 **P4-D 候选交付包**（`rei-school`、`rei-white`、`rei-black`），**须在 ChatGPT 主控对 P4-D 独立验收通过并正式授权进入 P5 后，再在 Windows 本地机执行安装与实机测试**。
> 2. **严禁修改或覆盖** `C:\Users\<user>\.codex\pets\` 下已存在的 3 套明日香宠物（`asuka-school`、`asuka-work`、`asuka-mixed-test`）及明日香参考工程。
> 3. 本阶段禁止提前标为正式 `v1.0.0` 发布；任何无法稳定触发的任务动画必须如实记为 **`NOT_TRIGGERED`**，严禁默认标 `PASS`。

---

## 1. 交付包清单与下载校验（只读）

从 GitHub 私有仓库（分支 `feat/p4d-final-assembly` 或经主控统一后的 `main`）下载以下独立安装包至独立临时目录（例如 `C:\Temp\rei-p5-verify\`）：

- `08_正式交付/P4-D-candidate/rei-school-codex-pet-v2.zip`（含 `rei-school/pet.json`、`rei-school/spritesheet.webp`）
- `08_正式交付/P4-D-candidate/rei-white-codex-pet-v2.zip`（含 `rei-white/pet.json`、`rei-white/spritesheet.webp`）
- `08_正式交付/P4-D-candidate/rei-black-codex-pet-v2.zip`（含 `rei-black/pet.json`、`rei-black/spritesheet.webp`）
- （可选总包）`08_正式交付/P4-D-candidate/rei-desktop-pet-p4d-all-3-bundle.zip`
- 哈希清单：`08_正式交付/P4-D-candidate/SHA256SUMS.txt` 与 `08_正式交付/P4-D-candidate/P4D_DELIVERY_MANIFEST.json`

### 1.1 解包与 SHA-256 核对（PowerShell 只读）

```powershell
$stage = "C:\Temp\rei-p5-verify"
foreach ($id in @("rei-school", "rei-white", "rei-black")) {
    Expand-Archive -Path "$stage\$id-codex-pet-v2.zip" -DestinationPath $stage -Force
}

Get-FileHash @(
    "$stage\rei-school-codex-pet-v2.zip",
    "$stage\rei-white-codex-pet-v2.zip",
    "$stage\rei-black-codex-pet-v2.zip",
    "$stage\rei-school\pet.json", "$stage\rei-school\spritesheet.webp",
    "$stage\rei-white\pet.json",  "$stage\rei-white\spritesheet.webp",
    "$stage\rei-black\pet.json",  "$stage\rei-black\spritesheet.webp"
) -Algorithm SHA256 | Format-Table Path, Hash -AutoSize
```

逐字符比对 `08_正式交付/P4-D-candidate/SHA256SUMS.txt`，确认全部一致后方可进入下一步。

---

## 2. Windows 原生 `validate_atlas.py --require-v2` 最终平台门禁（只读，不安装）

P4-D 云端/离线阶段**未执行** Windows MSIX 原生校验。P5 安装前，必须使用本机已安装的 `OpenAI.Codex` 随附 `hatch-pet\scripts\validate_atlas.py` 对三套 `spritesheet.webp` 逐一复检：

```powershell
$codexPkg = Get-AppxPackage -Name "OpenAI.Codex" | Select-Object -First 1
$validator = Join-Path $codexPkg.InstallLocation "app\resources\skills\skills\.curated\hatch-pet\scripts\validate_atlas.py"
Write-Host "Codex Version: $($codexPkg.Version)"
Write-Host "Validator: $validator"

foreach ($id in @("rei-school", "rei-white", "rei-black")) {
    Write-Host "=== Validating $id ==="
    python -B $validator "C:\Temp\rei-p5-verify\$id\spritesheet.webp" --require-v2 --json-out "C:\Temp\rei-p5-verify\$id-native-v2.json"
    Write-Host "EXIT_CODE=$LASTEXITCODE"
}
```

### 门禁要求（任一失败立即中止，禁止安装）
- 3 套均返回 `EXIT_CODE=0`、`ok: true`、`errors: []`、`warnings: []`；
- 3 套均为 `width=1536`、`height=2288`、`format="WEBP"`、`mode="RGBA"`、`sprite_version_number=2`、`transparent_rgb_residue_pixels=0`；
- `R0C6`（行 0 列 6 中性参考格）与第 9–10 行 16 个方向格全部识别为 `used: true`，14 个空格全部为 `0` 像素。

---

## 3. 安装前 Asuka 保护与冲突预检（只读）

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
foreach ($id in @("rei-school", "rei-white", "rei-black")) {
    $target = Join-Path $petsRoot $id
    if (Test-Path $target) {
        throw "ABORT: $target already exists! Inspect before continuing."
    }
}

Write-Host "=== Pre-P5 Asuka protection baseline (6 files) ==="
$asukaFiles = @(
    "$petsRoot\asuka-school\pet.json",
    "$petsRoot\asuka-school\spritesheet.webp",
    "$petsRoot\asuka-work\pet.json",
    "$petsRoot\asuka-work\spritesheet.webp",
    "$petsRoot\asuka-mixed-test\pet.json",
    "$petsRoot\asuka-mixed-test\spritesheet.webp"
)
Get-FileHash $asukaFiles -Algorithm SHA256 | Format-Table Path, Hash -AutoSize
```

同时记录当前 Codex Desktop 正在使用的默认宠物 ID，以便测试后随时安全切回。

---

## 4. 三套独立注册安装（须获 P5 明确授权后执行）

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
$stage = "C:\Temp\rei-p5-verify"

foreach ($id in @("rei-school", "rei-white", "rei-black")) {
    $dst = Join-Path $petsRoot $id
    New-Item -ItemType Directory -Path $dst -ErrorAction Stop | Out-Null
    Copy-Item "$stage\$id\pet.json" "$dst\pet.json" -ErrorAction Stop
    Copy-Item "$stage\$id\spritesheet.webp" "$dst\spritesheet.webp" -ErrorAction Stop
}
```

在 **Codex Desktop → Settings → Pets** 中刷新列表，核对：
- 新增显示三套独立宠物：**`绫波丽·校服`**（`custom:rei-school`）、**`绫波丽·白色战斗服00`**（`custom:rei-white`）、**`绫波丽·黑色战斗服09`**（`custom:rei-black`）；
- 原有 3 套 Asuka 宠物均正常保留且未被替换。

---

## 5. 分项实机运行验收清单（三形态逐套核验）

### 5.1 浮窗显示与明暗背景透明边缘
- [ ] **浅色背景**（白色记事本/浅色编辑器）：三形态轮廓清晰，无白边、黑框、矩形污斑或头顶/鞋尖裁切。
- [ ] **深色背景**（深色终端/黑色壁纸）：发尖、白袖、白服腿缝、黑服靴缘干净，无灰雾或透明区 RGB 残留。
- [ ] 标识核对：校服白发夹与红领结、白服胸口正写 `00` 与橙腕环、黑服胸口正写 `09` 与右手扶左臂在 1:1 桌面浮窗下清晰可辨。

### 5.2 鼠标 16 方向映射（顺时针逐扇区核对）
将鼠标围绕浮窗中心沿顺时针画一整圈，逐套核验 16 个扇区均自然跟随指针，无左右镜像反转、无跨行跳变：

| 鼠标相对浮窗方位 | 角度 | 预期图集格 | 核对要点 |
| --- | :---: | :---: | --- |
| 正上方（12 点） | `000°` | `R9C0` | 明确抬头/上视 |
| 右上偏上 / 右上 / 右上偏右 | `022.5° / 045° / 067.5°` | `R9C1–R9C3` | 顺时针渐进过渡，无突变 |
| 正右方（3 点） | `090°` | `R9C4` | 明确看向屏幕右 |
| 右下偏右 / 右下 / 右下偏下 | `112.5° / 135° / 157.5°` | `R9C5–R9C7` | 顺时针渐进过渡，无跳帧 |
| 正下方（6 点） | `180°` | `R10C0` | **重点检查 `157.5°→180°` 跨行衔接**，明确低头/下视 |
| 左下偏下 / 左下 / 左下偏左 | `202.5° / 225° / 247.5°` | `R10C1–R10C3` | 顺时针渐进过渡 |
| 正左方（9 点） | `270°` | `R10C4` | 明确看向屏幕左（非镜像反转） |
| 左上偏左 / 左上 / 左上偏上 | `292.5° / 315° / 337.5°` | `R10C5–R10C7` | **重点检查 `337.5°→000°` 回绕衔接** |

### 5.3 正中心死区与 `R0C6` 行为实测
- [ ] 将鼠标移至宠物正中心并静止：记录浮窗是否稳定回到正面中性外观、无闪动、无突兀缩放跳变（因 `R0C6` 与 `idle/00.png` 逐像素一致，无论渲染器采用 `R0C6` 还是回退 `idle`，视觉均应平滑无闪烁）。
- [ ] 将鼠标移离浮窗：确认 `idle` 循环（`R0C0–R0C5`）自然呼吸眨眼，无卡顿或多余帧闪现。

### 5.4 任务状态与交互动画（无法触发项严格记 `NOT_TRIGGERED`）
- [ ] `idle`（行 0，6 帧）：静止待机正常播放。
- [ ] `running-right`（行 1，8 帧）：水平向右拖动浮窗（≥ 4 屏幕单位）时播放向右小跑。
- [ ] `running-left`（行 2，8 帧）：水平向左拖动浮窗（≥ 4 屏幕单位）时播放向左小跑。
- [ ] `running`（行 7，6 帧）：发起常规 Codex 任务执行期间观察工作/专注姿态。
- [ ] `waiting`（行 6，6 帧）：触发需要审批/等待用户输入状态时观察等待姿态。
- [ ] `review`（行 8，6 帧）：任务完成未读提示/查看反馈时观察审阅姿态。
- [ ] `failed`（行 5，8 帧）：安全失败样本（如可控命令返回非零）触发时观察失败姿态。
- [ ] `waving`（行 3，4 帧）：首次唤醒（`first-awake`）时观察挥手姿态；未观察到记 `NOT_TRIGGERED`。
- [ ] `jumping`（行 4，5 帧）：若缺乏稳定触发入口，如实记 `NOT_TRIGGERED` 并引用 P4-B 离线 GIF 证据。

### 5.5 完全退出重启持久化
- [ ] 选中任意一套 Rei 宠物（建议逐套或至少重点抽验），**彻底退出 Codex Desktop（包含系统托盘右键退出，并用 `Get-Process *Codex*` / `Get-Process ChatGPT` 确认旧进程全部结束）**；
- [ ] 重新启动 Codex Desktop，核对浮窗自动恢复所选 Rei 宠物、无报错弹窗、无降级回退，且三套 Rei 与三套 Asuka 均仍在列表中可自由切换。

### 5.6 与已安装 Asuka 同尺寸画质比较（必做主观对照）
在同一桌面背景（浅色 + 深色）与同一显示缩放（DPI）下，依次切换 `asuka-school` ↔ `rei-school`、`asuka-work` ↔ `rei-white` / `rei-black`，逐项记录客观观感：
- [ ] **同尺寸视觉体量**：Rei（`188 px` 实体高，脚底 `(96, 195)`）与 Asuka（`194–198 px`）在桌面浮窗上的视觉大小比例是否协调自然；
- [ ] **线条清晰度与抗锯齿**：在原生浮窗显示尺寸下，线稿清晰度、发丝与服装边缘、胸口 `00`/`09` 字形清晰度与 Asuka 对比是否存在明显糊边或锯齿；
- [ ] **动作流畅度与方向连贯性**：待机、左右跑动、16 方向转头顺滑度与 Asuka 同尺寸对比体验记录；
- [ ] **透明通道洁净度**：明暗双底切换时，边缘泛白/泛灰控制是否不逊于或优于既有 Asuka 宠物。

---

## 6. 安全回退与 Asuka 完整性复核

如 P5 验收发现阻断问题或需要回退清理：
1. 在 **Codex Desktop → Settings → Pets** 中先切回原有 Asuka 宠物；
2. 仅删除需要回退的 `rei-school` / `rei-white` / `rei-black` 目录（严禁触碰 `asuka-*`）；
3. **云端迁移副本提示**：根据 P4-COMPAT 实机发现，`OpenAI.Codex 26.1120.6357.0` 加载本地自定义宠物时会自动在账号下建立云端同步副本（`migrated-cloud-pet-ids-v1`）；如需彻底撤回，请同步在 Codex Desktop Pets 界面中手动删除对应云端条目，**严禁直接修改 Codex 内部 SQLite 数据库**；
4. 复算全部 6 个 Asuka 文件 SHA-256，确认与安装前基线 100% 逐字节一致：

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
$asukaFiles = @(
    "$petsRoot\asuka-school\pet.json",
    "$petsRoot\asuka-school\spritesheet.webp",
    "$petsRoot\asuka-work\pet.json",
    "$petsRoot\asuka-work\spritesheet.webp",
    "$petsRoot\asuka-mixed-test\pet.json",
    "$petsRoot\asuka-mixed-test\spritesheet.webp"
)
Get-FileHash $asukaFiles -Algorithm SHA256 | Format-Table Path, Hash -AutoSize
```
