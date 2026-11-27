# WINDOWS_COMPAT_TEST_GUIDE.md｜Windows Codex Desktop Pets v2 原生兼容性验证指南

> **重要门禁声明**：
> 1. 本测试包 `rei-compat-test` 为 **P4-COMPAT 临时兼容性预验证包**，仅使用已有校服绫波丽 57 帧 + 16 个明确方向标识的临时测试格 + `(0,6)` 中性参考格，**不是正式 P4-C / P4-D / P5 发布版本**；临时方向素材**严禁**计入正式 P4-C 产物。
> 2. **实际本地安装需由用户明确另行批准后方可执行**；在批准安装前，可先在任意临时下载目录执行第 2 节的只读校验。
> 3. 全程**严禁修改或覆盖** `C:\Users\<user>\.codex\pets\` 下已存在的 3 套明日香宠物（`asuka-school`、`asuka-work`、`asuka-mixed-test`）及原本地工程 `D:\HuaweiMoveData\Users\86191\Desktop\Codex_Asuka`。

---

## 1. 可下载测试包与完整 SHA-256 核对清单

请从 GitHub 私有仓库（任务分支 `cloud-bootstrap/p4-compat-preverify`）下载以下文件至 Windows 临时目录（例如 `C:\Temp\rei-compat-download\`）：

| 文件 | 仓库相对路径 | 体积 (Bytes) | SHA-256 |
| --- | --- | ---: | --- |
| **一键下载压缩包** | `07_QA验收/P4-COMPAT/rei-compat-test.zip` | `803,543` | `9b36d7dd843aa65e76d17b7da63f876681edacbd9b23f7963bdf50b06e834fea` |
| 解包后清单文件 | `07_QA验收/P4-COMPAT/rei-compat-test/pet.json` | `349` | `f48cbc7e785e39698ad5f701fabd6556917be72e7b3bee7ddae036b0ad27913f` |
| 解包后 v2 图集 | `07_QA验收/P4-COMPAT/rei-compat-test/spritesheet.webp` | `802,834` | `bd6d29f401738015dddf452a79ffc460e6d53851f1ce691cbf25dd4605365201` |
| 离线 QA 报告 | `07_QA验收/P4-COMPAT/COMPAT_OFFLINE_QA.json` | — | 以本仓库实际提交为准 |
| 亮/暗底 11 行接触表 | `07_QA验收/P4-COMPAT/rei-compat-test-contact-sheet*.png` | — | 供肉眼对照 74 有效格 + 14 空格 |

### PowerShell 下载后哈希核验（只读，不安装）

```powershell
$dlDir = "C:\Temp\rei-compat-download"
Expand-Archive -Path "$dlDir\rei-compat-test.zip" -DestinationPath $dlDir -Force

Get-FileHash "$dlDir\rei-compat-test.zip",
             "$dlDir\rei-compat-test\pet.json",
             "$dlDir\rei-compat-test\spritesheet.webp" -Algorithm SHA256 |
  Format-Table -AutoSize
```

请确认输出 SHA-256 与上表逐字符一致后再继续。

---

## 2. 原生 `validate_atlas.py --require-v2` 校验方法（只读，无需安装）

使用本机已安装 Windows `OpenAI.Codex` MSIX 内置的官方 `hatch-pet\scripts\validate_atlas.py` 对解包后的 `spritesheet.webp` 执行真实 v2 门禁校验：

```powershell
# 自动定位当前已安装的 OpenAI.Codex MSIX 路径（兼容 26.1120.6357.0 及后续版本）
$codexPkg = Get-AppxPackage -Name "OpenAI.Codex" | Select-Object -First 1
$validator = Join-Path $codexPkg.InstallLocation "app\resources\skills\skills\.curated\hatch-pet\scripts\validate_atlas.py"

Write-Host "Codex Version: $($codexPkg.Version)"
Write-Host "Validator Path: $validator"

# 如使用固定历史路径，亦等价于：
# $validator = "C:\Program Files\WindowsApps\OpenAI.Codex_26.1120.6357.0_x64__2p2nqsd0c76g0\app\resources\skills\skills\.curated\hatch-pet\scripts\validate_atlas.py"

python -B $validator "C:\Temp\rei-compat-download\rei-compat-test\spritesheet.webp" --require-v2
Write-Host "EXIT_CODE=$LASTEXITCODE"
```

### 预期校验结果
- `EXIT_CODE=0`
- 输出 `"ok": true`、`"errors": []`、`"warnings": []`
- `width = 1536`、`height = 2288`、`format = "WEBP"`、`mode = "RGBA"`、`sprite_version_number = 2`
- `transparent_rgb_residue_pixels = 0`
- 行 0 列 6 `(0,6)` 中性参考格被识别为有效格（不再出现旧 Asuka v2 包的 `idle row 0 column 6 is empty or too sparse` 错误）

---

## 3. 安装前防止覆盖现有 Asuka 宠物的强制检查（只读）

> **仅当用户明确批准执行本地安装测试时，再继续第 3–4 节。**

在复制任何文件到 `$env:USERPROFILE\.codex\pets` 之前，先执行只读保护检查，确认：
1. 目标测试目录 `rei-compat-test` 当前**不存在**；
2. 已有 3 套明日香宠物目录及文件 SHA-256 完整记录为基线快照。

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
$targetDir = Join-Path $petsRoot "rei-compat-test"

if (Test-Path $targetDir) {
    throw "ABORT: $targetDir already exists! Please inspect before proceeding."
}

Write-Host "=== Existing pets directories ==="
Get-ChildItem $petsRoot -Directory | Select-Object Name, LastWriteTime

Write-Host "=== Pre-test Asuka protection hashes ==="
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

参考 P2 只读审计已记录的明日香宠物基线哈希（供比对）：
- `asuka-school\pet.json`: `8f22978ed8105d6b6e023377a5d550406fd220f3cdaeb59dbd429393366e7091`
- `asuka-work\pet.json`: `0dc5f4aa2a1c4accb0e0fc63ba0ca2cc5fa289f5195b0cf0885ae8454a43aa25`
- `asuka-mixed-test\pet.json`: `8fd1de1dd21b142947c71da042b8e65465c76bc9cb896ad3ab6ce55fdbbdba04`
- `asuka-mixed-test\spritesheet.webp`: `83aba65992452114a6a4156f6ec9655a3869b3a127b6ab0ce8edf15ccc865fcb`

---

## 4. 独立测试目录注册方法（需用户明确批准后执行）

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
$targetDir = Join-Path $petsRoot "rei-compat-test"
$srcDir = "C:\Temp\rei-compat-download\rei-compat-test"

# 1. 创建全新独立目录（不覆盖任何现有宠物）
New-Item -ItemType Directory -Path $targetDir -ErrorAction Stop | Out-Null

# 2. 仅复制 pet.json 与 spritesheet.webp
Copy-Item -Path "$srcDir\pet.json" -Destination "$targetDir\pet.json" -ErrorAction Stop
Copy-Item -Path "$srcDir\spritesheet.webp" -Destination "$targetDir\spritesheet.webp" -ErrorAction Stop

# 3. 安装后哈希复核
Get-FileHash "$targetDir\pet.json", "$targetDir\spritesheet.webp" -Algorithm SHA256 | Format-Table -AutoSize
```

### 在 Codex Desktop 中加载
1. 打开 **Codex Desktop** → 进入 **Settings → Pets**；
2. 点击刷新（Refresh）或在宠物列表中查找 **`Rei Compat Test (Temporary)`**（内部选择 ID 应为 `custom:rei-compat-test`）；
3. 确认已有 `asuka-school`、`asuka-work`、`asuka-mixed-test` 仍全部正常列出且未被替换；
4. 选择 **`Rei Compat Test (Temporary)`** 开启浮窗。

---

## 5. 实际浮窗显示、动画、鼠标方向映射与重启测试清单

请逐项实测并将结果填入 [WINDOWS_COMPAT_TEST_RESULT_TEMPLATE.json](WINDOWS_COMPAT_TEST_RESULT_TEMPLATE.json)：

### 5.1 浮窗显示与透明边缘测试
- [ ] 在**浅色**桌面背景/窗口前观察：人物边缘清晰、无白边/黑框/背景色块、无头顶或脚底裁切。
- [ ] 在**深色**桌面背景/窗口前观察：透明通道干净、无灰色污斑或隐藏 RGB 残留。

### 5.2 标准动画播放测试（行 0–8，校服绫波丽 57 帧）
- [ ] `idle`（行 0，6 帧）：静止待机时正常呼吸、眨眼，**且确认播放仅在列 0–5 循环，不会误将列 6 的 `NEUTRAL (0,6)` 混入待机循环**。
- [ ] `running-right`（行 1，8 帧）：水平向右拖动浮窗（横向位移 ≥ 4 屏幕单位）时切换为向右奔跑动画。
- [ ] `running-left`（行 2，8 帧）：水平向左拖动浮窗（横向位移 ≥ 4 屏幕单位）时切换为向左奔跑动画。
- [ ] `waving`（行 3，4 帧）：首次唤醒（`first-awake`）或对应触发入口时可见挥手动画（若本次未触发请在模板中如实记为 `NOT_TRIGGERED`）。
- [ ] `running` / `waiting` / `review` / `failed`（行 7 / 6 / 8 / 5）：如在普通任务或测试会话中观察到对应状态，分别记录实测状态与是否正常显示（未触发项记为 `NOT_TRIGGERED`，不臆测通过）。

### 5.3 鼠标 16 方向扇区映射与 `(0,6)` 中性死区实测（核心兼容性验证）
将鼠标围绕浮窗中心沿顺时针画一整圈，对照方向测试圆盘上的红色箭头与文字标签：

| 鼠标相对浮窗方位 | 预期角度 | 预期标签 | 预期图集格 | 核对要点 |
| --- | :---: | :---: | :---: | --- |
| 正上方（12 点） | `000°` | `N` | `R9C0` | 红色箭头严格指向上方 |
| 右上偏上 | `022.5°` | `NNE` | `R9C1` | 顺时针下一格 |
| 右上方 | `045°` | `NE` | `R9C2` | 45° 指向右上 |
| 右上偏右 | `067.5°` | `ENE` | `R9C3` | 顺时针下一格 |
| 正右方（3 点） | `090°` | `E` | `R9C4` | 红色箭头严格指向屏幕右 |
| 右下偏右 | `112.5°` | `ESE` | `R9C5` | 顺时针下一格 |
| 右下方 | `135°` | `SE` | `R9C6` | 135° 指向右下 |
| 右下偏下 | `157.5°` | `SSE` | `R9C7` | 第 9 行末格 |
| 正下方（6 点） | `180°` | `S` | `R10C0` | 跨行切换至第 10 行首格，箭头严格向下 |
| 左下偏下 | `202.5°` | `SSW` | `R10C1` | 顺时针下一格 |
| 左下方 | `225°` | `SW` | `R10C2` | 225° 指向左下 |
| 左下偏左 | `247.5°` | `WSW` | `R10C3` | 顺时针下一格 |
| 正左方（9 点） | `270°` | `W` | `R10C4` | 红色箭头严格指向屏幕左 |
| 左上偏左 | `292.5°` | `WNW` | `R10C5` | 顺时针下一格 |
| 左上方 | `315°` | `NW` | `R10C6` | 315° 指向左上 |
| 左上偏上 | `337.5°` | `NNW` | `R10C7` | 末格无缝回绕回 `000° N` |

- **关键实测问题（中心死区观察）**：将鼠标移到宠物正中心死区时，记录浮窗实际显示的是：
  - `NEUTRAL_CELL_0_6`（脚下带 `NEUTRAL (0,6)` 蓝色徽章的绫波丽），还是
  - `IDLE_FALLBACK`（不带徽章的正常 `idle` 帧），还是
  - `OTHER`（详述现象）。
  此实测结果将直接为正式 P4-C / P4-D 阶段提供第一手运行时真值。

### 5.4 重启持久化测试
1. 保持选中 `Rei Compat Test (Temporary)`；
2. 完全退出 **Codex Desktop**（含系统托盘图标退出，确保无残留进程）；
3. 重新启动 **Codex Desktop**；
4. 确认重启后浮窗仍正常恢复显示 `rei-compat-test`、无报错弹窗、无降级回退或图像丢失。

---

## 6. 安全回退与彻底移除方法

测试完成后，按以下步骤安全回退并移除临时测试包：

1. 先在 **Codex Desktop → Settings → Pets** 中将当前活动宠物切回你常用的明日香宠物（或关闭浮窗）；
2. 在 PowerShell 中仅删除 `rei-compat-test` 目录，并复核全部 3 套明日香宠物哈希未被改动：

```powershell
$petsRoot = Join-Path $env:USERPROFILE ".codex\pets"
$targetDir = Join-Path $petsRoot "rei-compat-test"

# 1. 仅移除临时测试目录
if (Test-Path $targetDir) {
    Remove-Item -Path $targetDir -Recurse -Force -Confirm
}

# 2. 确认 rei-compat-test 已彻底移除
Write-Host "rei-compat-test still exists? $(Test-Path $targetDir)"

# 3. 复核 3 套 Asuka 宠物哈希与测试前快照 100% 一致
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

3. 刷新 **Settings → Pets**，确认 `Rei Compat Test (Temporary)` 已从列表消失且原有明日香宠物正常运行。
4. 可选清理临时下载目录 `C:\Temp\rei-compat-download\`。
